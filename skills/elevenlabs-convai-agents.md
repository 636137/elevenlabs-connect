---
name: elevenlabs-convai-agents
description: "Build and embed ElevenLabs Conversational AI agents with working voice + text chat. Avoid common audio pitfalls."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Conversational AI Agents Skill

Build web-based AI voice agents using ElevenLabs Conversational AI platform.

## Related Skills

### ElevenLabs Suite
| Skill | Purpose |
|-------|---------|
| `elevenlabs-tts` | Text-to-Speech & Speech-to-Speech |
| `elevenlabs-voices` | Manage voices, clone, design |
| `elevenlabs-stt` | Speech-to-Text transcription |
| `elevenlabs-dubbing` | Video/audio dubbing |
| `elevenlabs-audio-tools` | Noise removal, sound FX, players |
| `elevenlabs-projects` | Long-form audiobooks/podcasts |
| `elevenlabs-admin` | Account, usage, history, models |

### UI Development Skills
| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `frontend-design` | Distinctive, production-grade frontend interfaces | Landing pages, dashboards, polished web UIs |
| `web-artifacts-builder` | Multi-component React/Tailwind/shadcn artifacts | Complex apps with state management, routing |

**For UI development**, invoke the appropriate skill:
- Simple/medium complexity pages → `frontend-design`
- Complex React applications → `web-artifacts-builder`

---

## UI Design Rules

**NEVER use emojis in the UI.** Use proper icons (SVG, icon libraries like Heroicons, Lucide, or Font Awesome) or text labels instead.

**Avoid generic "AI slop" aesthetics:**
- No purple gradients on white backgrounds
- No overused fonts (Inter, Roboto, Arial)
- No excessive centered layouts with uniform rounded corners
- No emoji as visual elements

---

## CRITICAL CHECKLIST - READ FIRST

Before debugging audio issues, verify ALL of these:

| # | Check | Required Value | How to Verify |
|---|-------|----------------|---------------|
| 1 | **Script URL** | `elevenlabs.io/convai-widget/index.js` | View page source |
| 2 | **Protocol** | `localhost:PORT` or `https://` | Check URL bar |
| 3 | **Browser cache** | Cleared | Cmd+Shift+R or clear site data |
| 4 | **Microphone permission** | Allowed | Click lock icon in URL bar |
| 5 | **Agent exists** | Valid agent_id | Test via API call |

### QUICK FIX FOR "AUDIO NOT SENT"

**90% of the time, the fix is:**
```
1. Cmd+Shift+R (hard refresh)
   — OR —
2. Chrome DevTools → Application tab → Storage → Clear site data
   — OR —  
3. Try incognito/private window
```

**The widget caches aggressively. After ANY changes, ALWAYS hard refresh.**

---

## CRITICAL: Widget Script Selection

**USE THIS SCRIPT** (audio works):
```html
<elevenlabs-convai agent-id="YOUR_AGENT_ID"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
```

**DO NOT USE** (audio broken):
```html
<!-- BROKEN - user audio not sent -->
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed"></script>
```

The `unpkg` package has a bug where user microphone audio is not transmitted. Always use the `elevenlabs.io` CDN script.

## Enabling Text Chat

Text chat is enabled via **agent configuration**, NOT widget attributes.

**Via API:**
```python
import requests

api_key = "your_api_key"
agent_id = "your_agent_id"

# Get current agent config
response = requests.get(
    f"https://api.elevenlabs.io/v1/convai/agents/{agent_id}",
    headers={"xi-api-key": api_key}
)
agent = response.json()

# Check if text input is enabled
text_enabled = agent["platform_settings"]["widget"]["text_input_enabled"]
print(f"Text input enabled: {text_enabled}")
```

**Via ElevenLabs Dashboard:**
1. Go to https://elevenlabs.io/app/conversational-ai
2. Select your agent
3. Widget Settings → Enable "Text Input"

## Localhost/HTTPS Requirement

**Browsers block microphone access on `file://` URLs.**

Always serve via localhost:
```bash
cd /path/to/your/html
python3 -m http.server 8000

# Then open:
# http://localhost:8000/your_page.html
```

Or deploy to HTTPS (GitHub Pages, Vercel, Netlify).

## Complete Working Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Demo</title>
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
        .container {
            text-align: center;
            padding: 40px;
        }
        h1 {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        p {
            color: rgba(255,255,255,0.7);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Voice Agent</h1>
        <p>Click the widget button (bottom-right) to start talking</p>
    </div>
    
    <!-- ElevenLabs Widget - USE THIS EXACT CONFIGURATION -->
    <elevenlabs-convai agent-id="YOUR_AGENT_ID"></elevenlabs-convai>
    <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
</body>
</html>
```

## API Reference

### List Agents
```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents" \
  -H "xi-api-key: YOUR_API_KEY"
```

### Get Agent Details
```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents/AGENT_ID" \
  -H "xi-api-key: YOUR_API_KEY"
```

### Create Agent
```python
import requests

payload = {
    "name": "My Agent",
    "conversation_config": {
        "agent": {
            "first_message": "Hello! How can I help you today?",
            "language": "en",
            "prompt": {
                "prompt": "You are a helpful assistant...",
                "llm": "gemini-2.0-flash-001",
                "temperature": 0.3,
                "max_tokens": 500
            }
        },
        "tts": {
            "model_id": "eleven_turbo_v2",
            "voice_id": "EXAVITQu4vr4xnSDxMaL"  # Sarah
        }
    },
    "platform_settings": {
        "widget": {
            "text_input_enabled": True,  # Enable chat
            "variant": "full"
        }
    }
}

response = requests.post(
    "https://api.elevenlabs.io/v1/convai/agents/create",
    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
    json=payload
)
```

## Troubleshooting

### Audio Not Sent (User Can't Be Heard)

**FIRST: Try the quick fix (solves 90% of issues):**
```
Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

**If that doesn't work, clear ALL site data:**
1. Open Chrome DevTools (F12 or Cmd+Option+I)
2. Go to **Application** tab
3. Click **Storage** in left sidebar
4. Click **Clear site data** button
5. Reload the page

**Chrome-specific issues? Try Safari/Firefox:**
Chrome has known WebRTC caching bugs with the ElevenLabs widget. If Chrome doesn't work after clearing site data:
- Test in **Safari** or **Firefox** - if it works there, it's Chrome
- Reset Chrome: `chrome://settings/reset` → "Restore settings to original defaults"
- Or use Chrome Incognito with all extensions disabled

**Still not working? Check these in order:**

| # | Check | Solution |
|---|-------|----------|
| 1 | Script URL | MUST be `elevenlabs.io/convai-widget/index.js` - NO unpkg |
| 2 | Protocol | MUST be `localhost:PORT` or `https://` - NO `file://` |
| 3 | Cache | Hard refresh: Cmd+Shift+R or clear site data |
| 4 | Permissions | Click lock icon in URL bar → Allow microphone |
| 5 | Browser | Try incognito window or different browser |
| 6 | Extensions | Disable ad blockers, privacy extensions |
| 7 | Agent | Verify agent_id exists via API |

### Why Caching Breaks Audio

The ElevenLabs widget caches WebRTC connection settings. If ANY of these change:
- Widget script version
- Agent configuration  
- Browser permissions
- Network conditions

...the cached connection info becomes stale and audio transmission fails silently.

**ALWAYS hard refresh after:**
- Changing agent settings
- Modifying the HTML
- Updating the widget script
- Granting microphone permissions
- Any debugging attempt

### No Text Input Box

| Check | Solution |
|-------|----------|
| Agent config | Enable `text_input_enabled` in dashboard or API |
| Widget script | Use `elevenlabs.io` script (supports agent config) |

### Widget Not Appearing

| Check | Solution |
|-------|----------|
| Agent ID | Verify agent exists via API |
| Script loading | Check console for 404 errors |
| Blockers | Disable ad blockers temporarily |

## Voice Options

| Voice ID | Name | Description |
|----------|------|-------------|
| EXAVITQu4vr4xnSDxMaL | Sarah | Professional female |
| 21m00Tcm4TlvDq8ikWAM | Rachel | Warm female |
| AZnzlk1XvdvUeBnXmlld | Domi | Strong female |
| MF3mGyEYCl7XYWbV9V6O | Emily | Calm female |
| TxGEqnHWrfWFTfGW9XjX | Josh | Deep male |
| VR6AewLTigWG4xSOukaG | Arnold | Narrative male |

## LLM Options

| Model ID | Provider | Speed |
|----------|----------|-------|
| gemini-2.0-flash-001 | Google | Fast |
| gpt-4o | OpenAI | Standard |
| claude-3-5-sonnet | Anthropic | Standard |

## References

- ElevenLabs Docs: https://elevenlabs.io/docs/conversational-ai
- Agent Dashboard: https://elevenlabs.io/app/conversational-ai
- API Reference: https://elevenlabs.io/docs/api-reference
