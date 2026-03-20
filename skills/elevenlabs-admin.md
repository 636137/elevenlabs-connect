---
name: elevenlabs-admin
description: "ElevenLabs account administration: user info, subscription details, usage tracking, history management, model information, and workspace settings."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Admin Skill

Manage your ElevenLabs account: check subscription limits, track usage, view generation history, list available models, and configure workspace settings.

## Related Skills
- `elevenlabs-tts` - Generate speech
- `elevenlabs-voices` - Manage voices
- `elevenlabs-convai-agents` - Manage AI agents

## API Endpoints

### User & Subscription
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/user` | GET | Get user info |
| `/v1/user/subscription` | GET | Get subscription details |

### History
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/history` | GET | List generation history |
| `/v1/history/{history_item_id}` | GET | Get history item |
| `/v1/history/{history_item_id}` | DELETE | Delete history item |
| `/v1/history/{history_item_id}/audio` | GET | Download audio |
| `/v1/history/download` | POST | Bulk download |

### Models
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/models` | GET | List all models |

### Workspace
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/workspace` | GET | Get workspace settings |
| `/v1/workspace/members` | GET | List workspace members |

---

## User & Subscription

### Get User Info
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

user = client.user.get()

print(f"User ID: {user.user_id}")
print(f"Email: {user.email}")
print(f"API Key: {user.xi_api_key_preview}")
print(f"Seat Type: {user.seat_type}")
```

### Get Subscription Details
```python
subscription = client.user.get_subscription()

print(f"Tier: {subscription.tier}")
print(f"Character Limit: {subscription.character_limit}")
print(f"Characters Used: {subscription.character_count}")
print(f"Characters Remaining: {subscription.character_limit - subscription.character_count}")
print(f"Voice Slots: {subscription.voice_slots}")
print(f"Max Voice Add Edits: {subscription.max_voice_add_edits}")
```

### cURL: Check Subscription
```bash
curl "https://api.elevenlabs.io/v1/user/subscription" \
  -H "xi-api-key: YOUR_API_KEY" | jq '{
    tier: .tier,
    character_limit: .character_limit,
    character_count: .character_count,
    remaining: (.character_limit - .character_count)
  }'
```

## Subscription Tiers

| Tier | Monthly Chars | Voices | Price |
|------|---------------|--------|-------|
| Free | 10,000 | 3 | $0 |
| Starter | 30,000 | 10 | $5/mo |
| Creator | 100,000 | 30 | $22/mo |
| Pro | 500,000 | 100 | $99/mo |
| Scale | 2,000,000 | Unlimited | $330/mo |

---

## History Management

### List Generation History
```python
history = client.history.get_all(
    page_size=50,
    voice_id="optional_filter_by_voice"
)

for item in history.history:
    print(f"ID: {item.history_item_id}")
    print(f"  Date: {item.date_unix}")
    print(f"  Text: {item.text[:50]}...")
    print(f"  Voice: {item.voice_name}")
    print(f"  Chars: {item.character_count_change_from}")
```

### Get Specific History Item
```python
item = client.history.get("history_item_id")

print(f"Text: {item.text}")
print(f"Voice: {item.voice_name}")
print(f"Model: {item.model_id}")
print(f"Characters: {item.character_count_change_from}")
print(f"Settings: {item.settings}")
```

### Download History Audio
```python
# Download single item
audio = client.history.get_audio("history_item_id")

with open("history_audio.mp3", "wb") as f:
    f.write(audio)

# Bulk download multiple items
bulk = client.history.download(
    history_item_ids=["id1", "id2", "id3"]
)

with open("bulk_download.zip", "wb") as f:
    f.write(bulk)
```

### Delete History Item
```python
client.history.delete("history_item_id")
print("Deleted!")
```

### Filter History
```python
# By voice
history = client.history.get_all(voice_id="voice_id")

# By model
history = client.history.get_all(model_id="eleven_turbo_v2")

# By date range
history = client.history.get_all(
    date_after_unix=1704067200,  # Jan 1, 2024
    date_before_unix=1706745600  # Feb 1, 2024
)

# By source
history = client.history.get_all(source="api")  # or "web"
```

---

## Models

### List All Models
```python
models = client.models.get_all()

for model in models:
    print(f"Model: {model.model_id}")
    print(f"  Name: {model.name}")
    print(f"  Description: {model.description}")
    print(f"  Can TTS: {model.can_do_text_to_speech}")
    print(f"  Can STS: {model.can_do_voice_conversion}")
    print(f"  Languages: {[l.name for l in model.languages]}")
```

### cURL: List Models
```bash
curl "https://api.elevenlabs.io/v1/models" \
  -H "xi-api-key: YOUR_API_KEY" | jq '.[] | {
    id: .model_id,
    name: .name,
    tts: .can_do_text_to_speech,
    sts: .can_do_voice_conversion
  }'
```

### Model Reference

| Model ID | Type | Languages | Best For |
|----------|------|-----------|----------|
| `eleven_v3` | TTS | 32 | Highest quality |
| `eleven_multilingual_v2` | TTS | 29 | International |
| `eleven_flash_v2_5` | TTS | 32 | Low latency |
| `eleven_turbo_v2_5` | TTS | 32 | Fast production |
| `eleven_turbo_v2` | TTS | 32 | Legacy turbo |
| `eleven_english_sts_v2` | STS | 1 | Voice conversion |
| `eleven_multilingual_sts_v2` | STS | 29 | Multilingual STS |
| `eleven_monolingual_v1` | TTS | 1 | Legacy English |
| `eleven_multilingual_v1` | TTS | 10 | Legacy multilingual |

---

## Workspace Management

### Get Workspace Settings
```python
workspace = client.workspace.get()

print(f"Workspace: {workspace}")
print(f"MCP Servers Enabled: {workspace.can_use_mcp_servers}")
print(f"RAG Retention Days: {workspace.rag_retention_period_days}")
```

### List Workspace Members (Enterprise)
```python
members = client.workspace.get_members()

for member in members.members:
    print(f"Member: {member.email}")
    print(f"  Role: {member.role}")
    print(f"  Status: {member.status}")
```

---

## Usage Tracking Dashboard

### Character Usage Report
```python
def usage_report():
    user = client.user.get()
    sub = client.user.get_subscription()
    
    used = sub.character_count
    limit = sub.character_limit
    pct = (used / limit) * 100 if limit > 0 else 0
    
    print("=" * 50)
    print("ELEVENLABS USAGE REPORT")
    print("=" * 50)
    print(f"Tier: {sub.tier}")
    print(f"Characters Used: {used:,} / {limit:,}")
    print(f"Usage: {pct:.1f}%")
    print(f"Remaining: {limit - used:,}")
    print("-" * 50)
    print(f"Voice Slots Used: {sub.voice_slots_used} / {sub.voice_slots}")
    print(f"Cloned Voices: {sub.cloned_voices_count}")
    print("=" * 50)

usage_report()
```

### Cost Tracking from API Calls
```python
def track_generation_cost(voice_id, text, model_id):
    """Generate TTS and track character cost."""
    
    # Use raw response to get headers
    response = client.text_to_speech.with_raw_response.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id
    )
    
    char_cost = response.headers.get("x-character-count")
    request_id = response.headers.get("request-id")
    
    print(f"Request ID: {request_id}")
    print(f"Characters Used: {char_cost}")
    
    return response.data, int(char_cost) if char_cost else 0
```

### Monthly Usage History
```python
import time
from datetime import datetime, timedelta

def monthly_usage_breakdown():
    """Get usage breakdown for current month."""
    
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    start_unix = int(start_of_month.timestamp())
    
    history = client.history.get_all(
        date_after_unix=start_unix,
        page_size=1000
    )
    
    # Aggregate by voice
    by_voice = {}
    for item in history.history:
        voice = item.voice_name or "Unknown"
        chars = item.character_count_change_from or 0
        by_voice[voice] = by_voice.get(voice, 0) + chars
    
    print(f"Usage for {now.strftime('%B %Y')}")
    print("-" * 40)
    for voice, chars in sorted(by_voice.items(), key=lambda x: -x[1]):
        print(f"  {voice}: {chars:,} chars")
    print("-" * 40)
    print(f"  Total: {sum(by_voice.values()):,} chars")

monthly_usage_breakdown()
```

---

## API Rate Limits

| Tier | Requests/min | Concurrent |
|------|--------------|------------|
| Free | 20 | 2 |
| Starter | 60 | 3 |
| Creator | 120 | 5 |
| Pro | 300 | 10 |
| Scale | 600 | 20 |

### Handle Rate Limits
```python
import time

def safe_request(func, *args, max_retries=3, **kwargs):
    """Execute with rate limit handling."""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "429" in str(e):  # Rate limit
                wait = 2 ** attempt
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## Error Reference

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid API key | Check `xi-api-key` header |
| 403 | Quota exceeded | Upgrade plan or wait for reset |
| 404 | Resource not found | Check ID exists |
| 429 | Rate limit | Implement backoff |
| 500 | Server error | Retry or contact support |

## Quick Commands

```bash
# Check remaining characters
curl -s "https://api.elevenlabs.io/v1/user/subscription" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" | \
  jq '{remaining: (.character_limit - .character_count)}'

# List recent generations
curl -s "https://api.elevenlabs.io/v1/history?page_size=5" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" | \
  jq '.history[] | {text: .text[:50], voice: .voice_name, chars: .character_count_change_from}'

# Get available models
curl -s "https://api.elevenlabs.io/v1/models" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" | \
  jq '.[].model_id'
```
