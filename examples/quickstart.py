#!/usr/bin/env python3
"""
Quick Start Example for ElevenLabs Conversational AI

This script demonstrates how to:
1. Create a new AI agent
2. List all agents in your account
3. Test the agent with a conversation

Prerequisites:
    pip install requests python-dotenv websockets
    
    Set your API key:
    export ELEVENLABS_API_KEY="your_key_here"
    
    Or create a .env file:
    ELEVENLABS_API_KEY=your_key_here

Author: Chad Hendren
"""

import os
import sys
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.create_agent import (
    create_elevenlabs_agent,
    list_agents,
    get_agent,
    VOICE_OPTIONS
)
from src.secure_setup import validate_api_key, mask_api_key
from src.test_agent import test_agent_conversation


def main():
    """
    Main example workflow demonstrating ElevenLabs agent creation and testing.
    """
    print("\n" + "=" * 60)
    print("ElevenLabs Conversational AI - Quick Start Example")
    print("=" * 60)
    
    # Step 1: Validate API key
    print("\n📋 Step 1: Validating API key...")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("❌ No API key found!")
        print("   Set ELEVENLABS_API_KEY environment variable or create .env file")
        sys.exit(1)
    
    is_valid, message = validate_api_key(api_key)
    if not is_valid:
        print(f"❌ Invalid API key: {message}")
        sys.exit(1)
    
    print(f"✅ API key valid: {mask_api_key(api_key)}")
    print(f"   {message}")
    
    # Step 2: List existing agents
    print("\n📋 Step 2: Listing existing agents...")
    agents = list_agents()
    
    if agents:
        print(f"   Found {len(agents)} agent(s):")
        for agent in agents[:5]:
            print(f"   - {agent['name']}: {agent['agent_id']}")
        if len(agents) > 5:
            print(f"   ... and {len(agents) - 5} more")
    else:
        print("   No agents found")
    
    # Step 3: Create a new agent (optional - uncomment to run)
    print("\n📋 Step 3: Creating a new agent...")
    print("   (Uncomment the code below to create an agent)")
    
    # Uncomment this section to create a new agent:
    # -----------------------------------------------
    # new_agent = create_elevenlabs_agent(
    #     name="Quick Start Demo Agent",
    #     first_message="Hello! I'm a demo agent created from the quick start guide. How can I help you today?",
    #     system_prompt="""You are a helpful demo assistant created to showcase ElevenLabs' Conversational AI capabilities.
    #     
    #     Your personality:
    #     - Friendly and professional
    #     - Concise but informative
    #     - Eager to demonstrate your capabilities
    #     
    #     When asked what you can do, explain that you can:
    #     - Answer questions and have natural conversations
    #     - Remember context within the current session
    #     - Speak with a natural-sounding voice
    #     
    #     Keep responses brief - 1-2 sentences when possible.""",
    #     voice_id=VOICE_OPTIONS["sarah"],  # Professional female voice
    #     tags=["demo", "quickstart"]
    # )
    # print(f"✅ Created agent: {new_agent['agent_id']}")
    # agent_id = new_agent['agent_id']
    # -----------------------------------------------
    
    # Step 4: Test an agent (requires an agent ID)
    print("\n📋 Step 4: Testing an agent...")
    
    if agents:
        # Use the first agent for testing
        agent_id = agents[0]['agent_id']
        print(f"   Testing agent: {agents[0]['name']} ({agent_id})")
        
        # Define test messages
        test_messages = [
            "Hello, what can you help me with?",
            "That sounds great, thanks!",
        ]
        
        # Run async test
        print("\n   Starting test conversation...")
        print("   " + "-" * 40)
        
        async def run_test():
            history = await test_agent_conversation(
                agent_id=agent_id,
                test_messages=test_messages
            )
            return history
        
        history = asyncio.run(run_test())
        
        print("\n✅ Test complete!")
        print(f"   Exchanged {len(history)} messages")
    else:
        print("   ⚠️ No agents available to test")
        print("   Create an agent first by uncommenting Step 3")
    
    print("\n" + "=" * 60)
    print("Quick Start complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
