"""
ElevenLabs Connect - Conversational AI Integration Package

This package provides tools for deploying and managing ElevenLabs
Conversational AI agents, with a focus on Amazon Connect integration.

Main Components:
    - create_agent: Create new conversational AI agents
    - manage_agents: List, update, and delete agents
    - test_agent: Run conversation tests against agents
    - secure_setup: Securely configure API credentials

Example:
    >>> from elevenlabs_connect import create_agent
    >>> agent = create_agent(
    ...     name="Support Bot",
    ...     first_message="Hello! How can I help?",
    ...     system_prompt="You are a helpful assistant."
    ... )
    >>> print(agent['agent_id'])

Author: Chad Hendren
Created: March 2026
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Chad Hendren"

from .create_agent import create_elevenlabs_agent, list_agents, get_agent
from .secure_setup import setup_credentials, validate_api_key
from .test_agent import test_agent_conversation

__all__ = [
    "create_elevenlabs_agent",
    "list_agents", 
    "get_agent",
    "setup_credentials",
    "validate_api_key",
    "test_agent_conversation",
]
