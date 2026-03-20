# ElevenLabs Connect

A comprehensive Python toolkit for building conversational AI voice agents with [ElevenLabs](https://elevenlabs.io). Create, deploy, and embed AI agents with natural voice capabilities.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Create AI Agents** - Deploy conversational agents with custom personalities and voices
- **Voice Synthesis** - Natural TTS powered by ElevenLabs turbo models
- **Secure Credentials** - Safe API key storage with masked input
- **Test Framework** - WebSocket-based agent testing
- **HTML Widget** - Embed agents in web pages with working audio
- **GitHub Copilot Skills** - AI-assisted development workflows

## Table of Contents

- [Quick Start](#quick-start)
- [Agent Examples](#agent-examples)
- [API Reference](#api-reference)
- [HTML Widget Integration](#html-widget-integration)
- [Copilot Skills](#copilot-skills)
- [UI Design Guidelines](#ui-design-guidelines)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

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

## Agent Examples

### Government Services Agent

```python
payload = {
    "name": "Texas Health and Human Services",
    "conversation_config": {
        "agent": {
            "first_message": "Hello, thank you for calling Texas Health and Human Services. How may I help you today?",
            "language": "en",
            "prompt": {
                "prompt": """You are a helpful assistant for Texas Health and Human Services.
Help callers with SNAP, Medicaid, TANF, WIC, and other assistance programs.
Key resources: YourTexasBenefits.com, 2-1-1 Texas hotline.
Be warm, patient, and use simple language.""",
                "llm": "gemini-2.0-flash-001",
                "temperature": 0.3,
                "max_tokens": 300
            }
        },
        "tts": {
            "model_id": "eleven_turbo_v2",
            "voice_id": "XrExE9yKIg1WjnnlVkGX"  # Matilda - warm, friendly
        }
    },
    "platform_settings": {
        "widget": {
            "text_input_enabled": True,
            "variant": "full"
        }
    }
}
```

### Customer Support Agent

```python
payload = {
    "name": "Support Assistant",
    "conversation_config": {
        "agent": {
            "first_message": "Hi! I'm here to help with any questions about our products or services.",
            "language": "en",
            "prompt": {
                "prompt": "You are a helpful customer support agent. Be concise and friendly.",
                "llm": "gemini-2.0-flash-001",
                "temperature": 0.3,
                "max_tokens": 256
            }
        },
        "tts": {
            "model_id": "eleven_turbo_v2",
            "voice_id": "EXAVITQu4vr4xnSDxMaL"  # Sarah
        }
    }
}
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

> **Important**: The endpoint is `/v1/convai/agents`, NOT `/v1/agents`

### Available LLM Models

| Model | Description |
|-------|-------------|
| `gemini-2.0-flash-001` | Fast, general purpose (recommended) |
| `gpt-4o` | OpenAI GPT-4o |
| `claude-3-5-sonnet` | Anthropic Claude |

### Voice Options

| Voice | ID | Style |
|-------|----|----|
| Sarah | `EXAVITQu4vr4xnSDxMaL` | Professional, reassuring |
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Classic, warm |
| Matilda | `XrExE9yKIg1WjnnlVkGX` | Warm, friendly |
| Josh | `TxGEqnHWrfWFTfGW9XjX` | Deep male |
| Antoni | `ErXwobaYiN019PkySvjV` | Well-rounded male |

### TTS Models

| Model | Speed | Notes |
|-------|-------|-------|
| `eleven_turbo_v2` | Fast | Required for English agents |
| `eleven_flash_v2` | Fastest | Good quality |
| `eleven_multilingual_v2` | Standard | Best for non-English |

## HTML Widget Integration

### Critical: Use the Correct Script

**USE THIS** (audio works):
```html
<elevenlabs-convai agent-id="YOUR_AGENT_ID"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
```

**DO NOT USE** (audio broken):
```html
<!-- BROKEN - user audio not sent -->
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed"></script>
```

### Complete Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Voice Agent</title>
    <style>
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container { text-align: center; padding: 40px; }
        h1 { font-size: 2.5rem; font-weight: 600; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Voice Agent</h1>
        <p>Click the widget button to start talking</p>
    </div>
    
    <elevenlabs-convai agent-id="YOUR_AGENT_ID"></elevenlabs-convai>
    <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
</body>
</html>
```

### Localhost Requirement

Browsers block microphone access on `file://` URLs. Always serve via localhost:

```bash
python3 -m http.server 8000
# Open: http://localhost:8000/your_page.html
```

## Copilot Skills

This project includes GitHub Copilot skills for AI-assisted development.

### Available Skills

| Skill | Purpose | Location |
|-------|---------|----------|
| `elevenlabs-convai-agents` | Build and embed ElevenLabs voice agents | `skills/elevenlabs-convai-agents.md` |

### Related Skills (install separately)

| Skill | Purpose |
|-------|---------|
| `frontend-design` | Create distinctive, production-grade frontend interfaces |
| `web-artifacts-builder` | Build complex React/Tailwind applications |
| `elevenlabs-tts` | Text-to-Speech synthesis |
| `elevenlabs-voices` | Voice management and cloning |

### Installing Skills

Copy skill files to your Copilot skills directory:

```bash
# macOS/Linux
mkdir -p ~/.copilot/skills/elevenlabs-convai-agents
cp skills/elevenlabs-convai-agents.md ~/.copilot/skills/elevenlabs-convai-agents/SKILL.md
```

## UI Design Guidelines

When building web interfaces for ElevenLabs agents:

### Do

- Use proper icons (SVG, Heroicons, Lucide, Font Awesome)
- Choose distinctive fonts (avoid Inter, Roboto, Arial)
- Create unique color schemes appropriate to the brand
- Use the `frontend-design` skill for polished UIs

### Don't

- **Never use emojis in the UI** - use proper icons instead
- Avoid purple gradients on white backgrounds
- Don't use cookie-cutter layouts
- Avoid generic "AI slop" aesthetics

### Recommended Approach

For UI development, invoke the appropriate Copilot skill:

- Simple/medium pages: `frontend-design` skill
- Complex React apps: `web-artifacts-builder` skill

## Troubleshooting

### Audio Not Sent (User Can't Be Heard)

**Quick fix (90% of issues):**
```
Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

**If that doesn't work:**
1. Chrome DevTools > Application > Storage > Clear site data
2. Try incognito/private window
3. Test in Safari or Firefox

### Checklist

| # | Check | Required |
|---|-------|----------|
| 1 | Script URL | `elevenlabs.io/convai-widget/index.js` |
| 2 | Protocol | `localhost:PORT` or `https://` |
| 3 | Cache | Cleared (hard refresh) |
| 4 | Permissions | Microphone allowed |
| 5 | Agent | Valid agent_id |

### Common Errors

| Error | Solution |
|-------|----------|
| 404 on agent creation | Use `/v1/convai/agents/create` not `/v1/agents` |
| 401 Unauthorized | Invalid API key - run `python -m src.secure_setup --check` |
| 403 Forbidden | Account tier doesn't support Conversational AI |

## Project Structure

```
elevenlabs-connect/
├── src/                          # Main library code
│   ├── __init__.py               # Package exports
│   ├── create_agent.py           # Agent creation functions
│   ├── secure_setup.py           # Credential management
│   └── test_agent.py             # Testing utilities
├── examples/                     # Example implementations
│   ├── quickstart.py             # Getting started script
│   └── widget_demo.html          # HTML widget example
├── skills/                       # GitHub Copilot skills
│   └── elevenlabs-convai-agents.md
├── tests/                        # Test suite
├── docs/                         # Documentation
├── AUDIO_TROUBLESHOOTING.md      # Audio debugging guide
├── .env.example                  # Environment template
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## Requirements

- Python 3.8+
- ElevenLabs API key (paid tier for Conversational AI)
- Dependencies: `requests`, `python-dotenv`, `websockets`

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as a template
2. **Use environment variables** - Don't hardcode API keys
3. **Restrict file permissions** - `.env` should be `0600`
4. **Validate keys** - Always validate before saving

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [ElevenLabs Documentation](https://elevenlabs.io/docs)
- [Conversational AI Docs](https://elevenlabs.io/docs/conversational-ai)
- [API Reference](https://elevenlabs.io/docs/api-reference)
- [Voice Library](https://elevenlabs.io/voice-library)

---

Created by Chad Hendren
