# ElevenLabs Connect

A Python library and toolkit for building conversational AI agents with [ElevenLabs](https://elevenlabs.io).

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- 🤖 **Create AI Agents** - Deploy conversational agents with custom personalities
- 🔊 **Voice Synthesis** - Natural TTS powered by ElevenLabs
- 🔒 **Secure Credentials** - Safe API key storage with masked input
- 🧪 **Test Framework** - WebSocket-based agent testing
- 📦 **HTML Widget** - Embed agents in web pages

## Quick Start

### 1. Installation

```bash
git clone https://github.com/636137/elevenlabs-connect.git
cd elevenlabs-connect
pip install -r requirements.txt
```

### 2. Set Up Credentials

Run the secure setup script:

```bash
python -m src.secure_setup
```

Or set the environment variable directly:

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

### 3. Create Your First Agent

```python
from src.create_agent import create_elevenlabs_agent

agent = create_elevenlabs_agent(
    name="Customer Support Bot",
    first_message="Hello! How can I help you today?",
    system_prompt="You are a friendly customer support agent.",
    voice_id="EXAVITQu4vr4xnSDxMaL"  # Sarah voice
)

print(f"Created agent: {agent['agent_id']}")
```

### 4. Test Your Agent

```python
import asyncio
from src.test_agent import test_agent_conversation

history = asyncio.run(test_agent_conversation(
    agent_id="your_agent_id",
    test_messages=["Hello!", "What can you do?"]
))
```

## API Reference

### Key Endpoints

ElevenLabs uses the **Conversational AI** API (`/v1/convai/`):

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Agents | GET | `/v1/convai/agents` |
| Create Agent | POST | `/v1/convai/agents/create` |
| Get Agent | GET | `/v1/convai/agents/{id}` |
| Update Agent | PUT | `/v1/convai/agents/{id}` |
| Delete Agent | DELETE | `/v1/convai/agents/{id}` |

> ⚠️ **Important**: The endpoint is `/v1/convai/agents`, NOT `/v1/agents`

### Agent Configuration

```python
payload = {
    "name": "Agent Name",
    "tags": ["tag1", "tag2"],
    "conversation_config": {
        "agent": {
            "first_message": "Hello!",
            "language": "en",
            "prompt": {
                "prompt": "System instructions...",
                "llm": "gemini-2.0-flash-001",
                "temperature": 0.3,
                "max_tokens": 500
            }
        },
        "tts": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",
            "model_id": "eleven_turbo_v2"
        }
    }
}
```

### Available LLM Models

| Model | Description |
|-------|-------------|
| `gemini-2.0-flash-001` | Fast, general purpose (recommended) |
| `gemini-2.5-flash` | Latest Google model |
| `gpt-4o` | OpenAI's most capable |
| `claude-3-sonnet` | Anthropic's balanced model |

### Voice Options

| Voice | ID | Style |
|-------|----|----|
| Sarah | `EXAVITQu4vr4xnSDxMaL` | Professional, reassuring |
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Classic, warm |
| Domi | `AZnzlk1XvdvUeBnXmlld` | Strong, clear |
| Antoni | `ErXwobaYiN019PkySvjV` | Well-rounded male |
| Josh | `TxGEqnHWrfWFTfGW9XjX` | Deep male |

## Project Structure

```
elevenlabs-connect/
├── src/                    # Main library code
│   ├── __init__.py         # Package exports
│   ├── create_agent.py     # Agent creation functions
│   ├── secure_setup.py     # Credential management
│   └── test_agent.py       # Testing utilities
├── examples/               # Example implementations
│   ├── quickstart.py       # Getting started script
│   └── widget_demo.html    # HTML widget example
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .env.example            # Environment template
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## HTML Widget Integration

Embed an agent in any webpage:

```html
<elevenlabs-convai agent-id="YOUR_AGENT_ID"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async></script>
```

See [examples/widget_demo.html](examples/widget_demo.html) for a complete example.

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as a template
2. **Use environment variables** - Don't hardcode API keys
3. **Restrict file permissions** - `.env` should be `0600` (owner read/write only)
4. **Validate keys** - Always validate before saving credentials

```python
from src.secure_setup import validate_api_key

is_valid, message = validate_api_key(api_key)
if is_valid:
    print(f"Key is valid: {message}")
```

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Code Style

This project follows PEP 8 with type hints:

```python
def create_agent(
    name: str,
    system_prompt: str,
    voice_id: str = DEFAULT_VOICE_ID
) -> Dict[str, Any]:
    """Create a new agent with the specified configuration."""
    ...
```

## Troubleshooting

### 404 Error on Agent Creation

Make sure you're using the correct endpoint:
- ✅ Correct: `/v1/convai/agents/create`
- ❌ Wrong: `/v1/agents`

### 401 Unauthorized

Your API key may be invalid or expired. Run:

```bash
python -m src.secure_setup --check
```

### 403 Forbidden

Your account tier may not support Conversational AI. Check your subscription at [elevenlabs.io/app/subscription](https://elevenlabs.io/app/subscription).

### WebSocket Connection Failed

Ensure you're using the signed URL endpoint:

```python
url = f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url"
params = {"agent_id": agent_id}
```

## Requirements

- Python 3.8+
- ElevenLabs API key (paid tier for Conversational AI)
- Dependencies:
  - `requests`
  - `python-dotenv`
  - `websockets`

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [ElevenLabs Documentation](https://elevenlabs.io/docs)
- [Conversational AI Docs](https://elevenlabs.io/docs/conversational-ai)
- [API Reference](https://elevenlabs.io/docs/api-reference)
- [Voice Library](https://elevenlabs.io/voice-library)

---

Created by Chad Hendren • March 2026
