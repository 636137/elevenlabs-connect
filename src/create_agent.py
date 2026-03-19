#!/usr/bin/env python3
"""
ElevenLabs Conversational AI Agent Creation Module

This module provides functions to create, configure, and manage
ElevenLabs Conversational AI agents via the API.

CRITICAL API NOTE:
    The correct endpoint is /v1/convai/agents (NOT /v1/agents!)
    - List agents:   GET  /v1/convai/agents
    - Create agent:  POST /v1/convai/agents/create
    - Get agent:     GET  /v1/convai/agents/{agent_id}
    - Update agent:  PUT  /v1/convai/agents/{agent_id}

Available LLM Models:
    - gemini-2.0-flash-001: Fast, general purpose (recommended)
    - gemini-2.5-flash: Latest Google model
    - gpt-4o: OpenAI's most capable model
    - claude-3-sonnet: Anthropic's balanced model

Example:
    >>> from create_agent import create_elevenlabs_agent
    >>> agent = create_elevenlabs_agent(
    ...     name="Customer Support",
    ...     first_message="Hello! How can I help you today?",
    ...     system_prompt="You are a helpful customer service agent.",
    ...     voice_id="EXAVITQu4vr4xnSDxMaL"  # Sarah voice
    ... )
    >>> print(f"Created agent: {agent['agent_id']}")

Author: Chad Hendren
Created: March 2026
"""

import os
import json
import logging
from typing import Optional, Dict, List, Any
from pathlib import Path

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# API Configuration
# IMPORTANT: The correct base path is /v1/convai/ for Conversational AI
API_BASE_URL = "https://api.elevenlabs.io/v1"
CONVAI_BASE = f"{API_BASE_URL}/convai"  # Conversational AI endpoints

# Default voice settings
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Sarah - professional, reassuring
DEFAULT_TTS_MODEL = "eleven_turbo_v2"  # Fastest model, ~40ms latency
DEFAULT_LLM = "gemini-2.0-flash-001"  # Fast, good for support scenarios


def get_api_key() -> str:
    """
    Retrieve the ElevenLabs API key from environment variables.
    
    The key should be stored in a .env file (gitignored) or as
    an environment variable named ELEVENLABS_API_KEY.
    
    Returns:
        str: The API key
        
    Raises:
        ValueError: If API key is not found
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY not found. "
            "Set it in your .env file or environment variables."
        )
    return api_key


def _make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    api_key: Optional[str] = None
) -> Dict:
    """
    Make an authenticated request to the ElevenLabs API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path (will be appended to CONVAI_BASE)
        data: JSON body for POST/PUT requests
        params: Query parameters
        api_key: Optional API key (uses environment if not provided)
    
    Returns:
        dict: JSON response from the API
        
    Raises:
        requests.HTTPError: If the request fails
    """
    api_key = api_key or get_api_key()
    
    # Build full URL - using convai base for agent endpoints
    url = f"{CONVAI_BASE}{endpoint}"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    logger.debug(f"Making {method} request to {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Raise exception for error status codes
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"API error: {e.response.status_code} - {e.response.text}")
        raise
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise


def create_elevenlabs_agent(
    name: str,
    first_message: str,
    system_prompt: str,
    voice_id: str = DEFAULT_VOICE_ID,
    llm: str = DEFAULT_LLM,
    tags: Optional[List[str]] = None,
    temperature: float = 0.3,
    max_tokens: int = 500,
    max_duration_seconds: int = 600,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new ElevenLabs Conversational AI agent.
    
    This function creates a fully configured agent with voice, LLM,
    and conversation settings. The agent can then be tested via the
    dashboard, embedded in a webpage, or integrated with telephony.
    
    Args:
        name: Human-readable agent name (e.g., "Customer Support Bot")
        first_message: What the agent says when a conversation starts
        system_prompt: Instructions that guide agent behavior
        voice_id: ElevenLabs voice ID (default: Sarah - professional)
        llm: Language model to use (default: gemini-2.0-flash-001)
        tags: Optional list of tags for organization
        temperature: LLM temperature (0.0-1.0, lower = more deterministic)
        max_tokens: Maximum tokens per response
        max_duration_seconds: Maximum conversation duration (default: 10 min)
        api_key: Optional API key (uses environment if not provided)
    
    Returns:
        dict: Agent configuration including the generated agent_id
        
    Example:
        >>> agent = create_elevenlabs_agent(
        ...     name="IRS Taxpayer Assistant",
        ...     first_message="Hello! I can help with refunds and payments.",
        ...     system_prompt="You are a professional IRS assistant...",
        ...     voice_id="EXAVITQu4vr4xnSDxMaL",
        ...     tags=["IRS", "Government", "Support"]
        ... )
        >>> print(agent['agent_id'])
        'agent_abc123xyz'
    """
    logger.info(f"Creating agent: {name}")
    
    # Build the agent configuration payload
    # This structure matches the ElevenLabs Conversational AI API schema
    payload = {
        "name": name,
        "tags": tags or [],
        "conversation_config": {
            # Agent behavior configuration
            "agent": {
                "first_message": first_message,
                "language": "en",
                "prompt": {
                    "prompt": system_prompt,
                    "llm": llm,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            },
            # Text-to-Speech configuration
            "tts": {
                "voice_id": voice_id,
                "model_id": DEFAULT_TTS_MODEL,
                "stability": 0.5,  # Balance between variation and consistency
                "similarity_boost": 0.75,
                "optimize_streaming_latency": 3  # Optimize for low latency
            },
            # Turn-taking configuration
            "turn": {
                "turn_timeout": 10,  # Seconds before agent assumes user is done
                "silence_end_call_timeout": 30,  # End call after this silence
                "turn_eagerness": "normal"  # How quickly agent responds
            },
            # Conversation settings
            "conversation": {
                "max_duration_seconds": max_duration_seconds,
                "text_only": False  # Enable voice
            }
        }
    }
    
    # Make the API request to create the agent
    # IMPORTANT: Endpoint is /agents/create (not just /agents)
    result = _make_request("POST", "/agents/create", data=payload, api_key=api_key)
    
    agent_id = result.get("agent_id")
    logger.info(f"Agent created successfully: {agent_id}")
    
    return result


def list_agents(
    page_size: int = 30,
    search: Optional[str] = None,
    archived: Optional[bool] = None,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    List all conversational AI agents in the account.
    
    Args:
        page_size: Number of agents to return (max 100)
        search: Filter by agent name
        archived: Filter by archived status
        api_key: Optional API key
    
    Returns:
        list: List of agent metadata dictionaries
        
    Example:
        >>> agents = list_agents()
        >>> for agent in agents:
        ...     print(f"{agent['name']}: {agent['agent_id']}")
    """
    logger.info("Listing agents...")
    
    params = {"page_size": min(page_size, 100)}
    if search:
        params["search"] = search
    if archived is not None:
        params["archived"] = archived
    
    result = _make_request("GET", "/agents", params=params, api_key=api_key)
    
    agents = result.get("agents", [])
    logger.info(f"Found {len(agents)} agents")
    
    return agents


def get_agent(agent_id: str, api_key: Optional[str] = None) -> Dict:
    """
    Get detailed configuration for a specific agent.
    
    Args:
        agent_id: The agent's unique identifier
        api_key: Optional API key
    
    Returns:
        dict: Complete agent configuration
        
    Example:
        >>> agent = get_agent("agent_abc123xyz")
        >>> print(agent['conversation_config']['agent']['first_message'])
    """
    logger.info(f"Getting agent: {agent_id}")
    
    result = _make_request("GET", f"/agents/{agent_id}", api_key=api_key)
    
    return result


def update_agent(
    agent_id: str,
    updates: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict:
    """
    Update an existing agent's configuration.
    
    Args:
        agent_id: The agent's unique identifier
        updates: Dictionary of fields to update
        api_key: Optional API key
    
    Returns:
        dict: Updated agent configuration
    """
    logger.info(f"Updating agent: {agent_id}")
    
    result = _make_request("PUT", f"/agents/{agent_id}", data=updates, api_key=api_key)
    
    return result


def delete_agent(agent_id: str, api_key: Optional[str] = None) -> bool:
    """
    Delete an agent (archives it).
    
    Args:
        agent_id: The agent's unique identifier
        api_key: Optional API key
    
    Returns:
        bool: True if deletion was successful
    """
    logger.info(f"Deleting agent: {agent_id}")
    
    try:
        _make_request("DELETE", f"/agents/{agent_id}", api_key=api_key)
        return True
    except Exception as e:
        logger.error(f"Failed to delete agent: {e}")
        return False


# Voice ID reference for common voices
VOICE_OPTIONS = {
    "sarah": "EXAVITQu4vr4xnSDxMaL",  # Professional, reassuring
    "rachel": "21m00Tcm4TlvDq8ikWAM",  # Classic, warm
    "domi": "AZnzlk1XvdvUeBnXmlld",    # Strong, clear
    "bella": "EXAVITKu4r8xnSDxMaL",    # Young, friendly
    "antoni": "ErXwobaYiN019PkySvjV",  # Well-rounded male
    "josh": "TxGEqnHWrfWFTfGW9XjX",    # Deep male
}


if __name__ == "__main__":
    # Example usage when run directly
    import sys
    
    print("ElevenLabs Conversational AI Agent Creator")
    print("=" * 50)
    
    try:
        # List existing agents
        agents = list_agents()
        print(f"\nFound {len(agents)} existing agents:")
        for agent in agents[:5]:
            print(f"  - {agent.get('name')}: {agent.get('agent_id')}")
        
        if len(agents) > 5:
            print(f"  ... and {len(agents) - 5} more")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
