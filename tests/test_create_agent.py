#!/usr/bin/env python3
"""
Test suite for create_agent module

Run with: pytest tests/ -v
"""

import os
import pytest
from unittest.mock import patch, MagicMock

# Add src to path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.create_agent import (
    get_api_key,
    create_elevenlabs_agent,
    list_agents,
    get_agent,
    VOICE_OPTIONS
)


class TestGetApiKey:
    """Tests for get_api_key function."""
    
    def test_get_api_key_from_env(self):
        """Should retrieve API key from environment."""
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key_123'}):
            key = get_api_key()
            assert key == 'test_key_123'
    
    def test_get_api_key_missing(self):
        """Should raise ValueError when key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('ELEVENLABS_API_KEY', None)
            with pytest.raises(ValueError, match="ELEVENLABS_API_KEY not found"):
                get_api_key()


class TestVoiceOptions:
    """Tests for voice configuration."""
    
    def test_voice_options_has_sarah(self):
        """Sarah voice should be available."""
        assert 'sarah' in VOICE_OPTIONS
        assert VOICE_OPTIONS['sarah'] == 'EXAVITQu4vr4xnSDxMaL'
    
    def test_voice_options_complete(self):
        """All standard voices should be available."""
        expected_voices = ['sarah', 'rachel', 'domi', 'bella', 'antoni', 'josh']
        for voice in expected_voices:
            assert voice in VOICE_OPTIONS


class TestCreateAgent:
    """Tests for create_elevenlabs_agent function."""
    
    @patch('src.create_agent._make_request')
    def test_create_agent_basic(self, mock_request):
        """Should create agent with basic parameters."""
        mock_request.return_value = {'agent_id': 'agent_test123'}
        
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key'}):
            result = create_elevenlabs_agent(
                name="Test Agent",
                first_message="Hello!",
                system_prompt="You are a test agent."
            )
        
        assert result['agent_id'] == 'agent_test123'
        mock_request.assert_called_once()
    
    @patch('src.create_agent._make_request')
    def test_create_agent_with_custom_voice(self, mock_request):
        """Should pass custom voice_id in request."""
        mock_request.return_value = {'agent_id': 'agent_test456'}
        
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key'}):
            create_elevenlabs_agent(
                name="Custom Voice Agent",
                first_message="Hello!",
                system_prompt="Test.",
                voice_id="custom_voice_id"
            )
        
        # Verify the payload included custom voice
        call_args = mock_request.call_args
        payload = call_args[1]['data']
        assert payload['conversation_config']['tts']['voice_id'] == 'custom_voice_id'


class TestListAgents:
    """Tests for list_agents function."""
    
    @patch('src.create_agent._make_request')
    def test_list_agents_empty(self, mock_request):
        """Should handle empty agent list."""
        mock_request.return_value = {'agents': []}
        
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key'}):
            result = list_agents()
        
        assert result == []
    
    @patch('src.create_agent._make_request')
    def test_list_agents_returns_list(self, mock_request):
        """Should return list of agents."""
        mock_request.return_value = {
            'agents': [
                {'agent_id': 'agent_1', 'name': 'Agent 1'},
                {'agent_id': 'agent_2', 'name': 'Agent 2'}
            ]
        }
        
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key'}):
            result = list_agents()
        
        assert len(result) == 2
        assert result[0]['agent_id'] == 'agent_1'
