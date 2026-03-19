#!/usr/bin/env python3
"""
ElevenLabs Agent Testing Module

This module provides utilities for testing ElevenLabs Conversational AI
agents via WebSocket connections. It allows you to have text-based
conversations with your agents for testing and debugging.

Features:
    - WebSocket-based conversation with agents
    - Real-time streaming responses
    - Conversation history tracking
    - Debug mode for detailed logging

Note:
    For voice testing, use the HTML widget or the ElevenLabs dashboard.
    This module is primarily for text-based API testing.

Author: Chad Hendren
Created: March 2026
"""

import os
import json
import asyncio
import logging
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime

import websockets
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# WebSocket endpoint for signed URLs
# This endpoint creates a secure session for agent conversation
WS_URL_BASE = "wss://api.elevenlabs.io/v1/convai/conversation"


class ConversationMessage:
    """
    Represents a single message in a conversation.
    
    Attributes:
        role: Either "user" or "agent"
        content: The message text
        timestamp: When the message was sent/received
    """
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        return f"[{self.role.upper()}] {self.content}"


class AgentTester:
    """
    Test harness for ElevenLabs Conversational AI agents.
    
    This class manages WebSocket connections to agents and provides
    methods for sending messages and processing responses.
    
    Example:
        >>> tester = AgentTester(agent_id="agent_abc123")
        >>> await tester.connect()
        >>> response = await tester.send_message("Hello!")
        >>> print(response)
        >>> await tester.disconnect()
    """
    
    def __init__(
        self,
        agent_id: str,
        api_key: Optional[str] = None,
        debug: bool = False
    ):
        """
        Initialize the agent tester.
        
        Args:
            agent_id: The ElevenLabs agent ID to test
            api_key: Optional API key (uses environment if not provided)
            debug: Enable detailed debug logging
        """
        self.agent_id = agent_id
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.debug = debug
        
        # Connection state
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._conversation_id: Optional[str] = None
        
        # Conversation history
        self.history: List[ConversationMessage] = []
        
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
    
    async def _get_signed_url(self) -> str:
        """
        Get a signed WebSocket URL for the agent.
        
        ElevenLabs requires authenticated URLs for WebSocket connections.
        This fetches a signed URL that's valid for a limited time.
        
        Returns:
            str: Signed WebSocket URL
        """
        import requests  # Import here to avoid async issues
        
        url = f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url"
        params = {"agent_id": self.agent_id}
        headers = {"xi-api-key": self.api_key}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        signed_url = data.get("signed_url")
        
        if not signed_url:
            raise ValueError("No signed URL in response")
        
        logger.debug(f"Got signed URL for agent {self.agent_id}")
        return signed_url
    
    async def connect(self) -> None:
        """
        Establish WebSocket connection to the agent.
        
        Must be called before sending messages.
        """
        if self._websocket:
            logger.warning("Already connected, disconnecting first")
            await self.disconnect()
        
        try:
            signed_url = await self._get_signed_url()
            
            logger.info(f"Connecting to agent {self.agent_id}...")
            self._websocket = await websockets.connect(signed_url)
            
            # Wait for initial connection confirmation
            init_message = await asyncio.wait_for(
                self._websocket.recv(),
                timeout=10
            )
            init_data = json.loads(init_message)
            
            if init_data.get("type") == "conversation_initiation_metadata":
                self._conversation_id = init_data.get("conversation_initiation_metadata_event", {}).get("conversation_id")
                logger.info(f"Connected! Conversation ID: {self._conversation_id}")
            else:
                logger.debug(f"Init message: {init_data}")
                
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close the WebSocket connection."""
        if self._websocket:
            await self._websocket.close()
            self._websocket = None
            self._conversation_id = None
            logger.info("Disconnected from agent")
    
    async def send_message(
        self,
        message: str,
        on_audio_chunk: Optional[Callable[[bytes], None]] = None
    ) -> str:
        """
        Send a text message to the agent and get the response.
        
        Args:
            message: The text message to send
            on_audio_chunk: Optional callback for audio chunks
            
        Returns:
            str: The agent's text response
        """
        if not self._websocket:
            raise RuntimeError("Not connected. Call connect() first.")
        
        # Record user message
        user_msg = ConversationMessage("user", message)
        self.history.append(user_msg)
        logger.debug(f"Sending: {message}")
        
        # Send user message
        await self._websocket.send(json.dumps({
            "type": "user_input",
            "user_input": {"text": message}
        }))
        
        # Collect response
        response_text = ""
        audio_chunks = []
        
        try:
            while True:
                raw_message = await asyncio.wait_for(
                    self._websocket.recv(),
                    timeout=30
                )
                data = json.loads(raw_message)
                msg_type = data.get("type")
                
                if self.debug:
                    logger.debug(f"Received: {msg_type} - {data}")
                
                # Handle different message types
                if msg_type == "agent_response":
                    # Agent's text response
                    text_chunk = data.get("agent_response_event", {}).get("agent_response", "")
                    response_text += text_chunk
                    
                elif msg_type == "audio":
                    # Audio chunk (base64 encoded)
                    audio_data = data.get("audio_event", {}).get("audio_base_64")
                    if audio_data and on_audio_chunk:
                        import base64
                        decoded = base64.b64decode(audio_data)
                        on_audio_chunk(decoded)
                        audio_chunks.append(decoded)
                        
                elif msg_type == "agent_response_correction":
                    # The agent may correct its response
                    response_text = data.get("agent_response_correction_event", {}).get("corrected_response", response_text)
                    
                elif msg_type == "turn_ended":
                    # Agent finished speaking
                    logger.debug("Agent turn ended")
                    break
                    
                elif msg_type == "ping":
                    # Keep-alive ping, send pong
                    await self._websocket.send(json.dumps({"type": "pong"}))
                    
        except asyncio.TimeoutError:
            logger.warning("Response timeout")
        
        # Record agent response
        if response_text:
            agent_msg = ConversationMessage("agent", response_text)
            self.history.append(agent_msg)
        
        return response_text
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history as a list of dictionaries.
        
        Returns:
            list: Conversation messages
        """
        return [msg.to_dict() for msg in self.history]
    
    def print_history(self) -> None:
        """Print the conversation history to console."""
        print("\n" + "=" * 60)
        print("CONVERSATION HISTORY")
        print("=" * 60)
        for msg in self.history:
            prefix = "👤 USER  " if msg.role == "user" else "🤖 AGENT "
            print(f"\n{prefix} ({msg.timestamp.strftime('%H:%M:%S')})")
            print(f"   {msg.content}")
        print("=" * 60 + "\n")


async def test_agent_conversation(
    agent_id: str,
    test_messages: List[str],
    api_key: Optional[str] = None,
    debug: bool = False
) -> List[Dict[str, Any]]:
    """
    Run a test conversation with an agent.
    
    This function connects to the specified agent, sends a series
    of test messages, and returns the full conversation history.
    
    Args:
        agent_id: The ElevenLabs agent ID to test
        test_messages: List of messages to send in order
        api_key: Optional API key
        debug: Enable debug logging
        
    Returns:
        list: Full conversation history
        
    Example:
        >>> history = await test_agent_conversation(
        ...     agent_id="agent_abc123",
        ...     test_messages=[
        ...         "What's my refund status?",
        ...         "It's 123-45-6789",
        ...         "Thank you, goodbye"
        ...     ]
        ... )
        >>> for msg in history:
        ...     print(f"{msg['role']}: {msg['content']}")
    """
    tester = AgentTester(agent_id, api_key, debug)
    
    try:
        await tester.connect()
        
        print(f"\n🧪 Testing agent: {agent_id}")
        print("=" * 50)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📤 [{i}/{len(test_messages)}] Sending: {message}")
            
            response = await tester.send_message(message)
            
            print(f"📥 Response: {response}")
        
        print("\n" + "=" * 50)
        print("✅ Test complete!")
        
        return tester.get_history()
        
    finally:
        await tester.disconnect()


def quick_test(agent_id: str, message: str = "Hello!") -> str:
    """
    Synchronous wrapper for quick single-message tests.
    
    Args:
        agent_id: The agent to test
        message: Single message to send
        
    Returns:
        str: Agent's response
    """
    async def _test():
        tester = AgentTester(agent_id)
        await tester.connect()
        response = await tester.send_message(message)
        await tester.disconnect()
        return response
    
    return asyncio.run(_test())


if __name__ == "__main__":
    """
    Interactive testing mode when run directly.
    
    Usage:
        python test_agent.py <agent_id>
        python test_agent.py <agent_id> --debug
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_agent.py <agent_id> [--debug]")
        print("\nExample:")
        print("  python test_agent.py agent_abc123xyz")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    debug = "--debug" in sys.argv
    
    async def interactive_test():
        tester = AgentTester(agent_id, debug=debug)
        
        try:
            await tester.connect()
            
            print("\n" + "=" * 50)
            print(f"Connected to agent: {agent_id}")
            print("Type your messages. Enter 'quit' to exit.")
            print("=" * 50 + "\n")
            
            while True:
                try:
                    user_input = input("\n👤 You: ").strip()
                except EOFError:
                    break
                
                if user_input.lower() in ('quit', 'exit', 'q'):
                    break
                
                if not user_input:
                    continue
                
                response = await tester.send_message(user_input)
                print(f"\n🤖 Agent: {response}")
            
            tester.print_history()
            
        finally:
            await tester.disconnect()
    
    asyncio.run(interactive_test())
