---
name: elevenlabs-voices
description: "Manage ElevenLabs voices: list, clone, design, configure settings. Search the voice library, manage samples, and create custom voices."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Voices Skill

Manage voices for text-to-speech: list available voices, clone voices from audio, design synthetic voices, and configure voice settings.

## Related Skills
- `elevenlabs-tts` - Use voices for speech generation
- `elevenlabs-convai-agents` - Use voices in AI agents
- `elevenlabs-admin` - Check voice quotas

## API Endpoints

### Voice Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/voices` | GET | List all your voices |
| `/v1/voices/{voice_id}` | GET | Get voice details |
| `/v1/voices/{voice_id}` | DELETE | Delete a voice |
| `/v1/voices/add` | POST | Clone/add a voice |

### Voice Settings
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/voices/{voice_id}/settings` | GET | Get voice settings |
| `/v1/voices/{voice_id}/settings/edit` | POST | Update settings |

### Voice Library (Shared)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/shared-voices` | GET | Browse voice library |

### Voice Design
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/voice-generation/generate-voice` | POST | Create synthetic voice |
| `/v1/voice-generation/generate-voice/parameters` | GET | Get design options |

### Voice Samples
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/voices/{voice_id}/samples` | GET | List samples |
| `/v1/voices/{voice_id}/samples/{sample_id}` | DELETE | Delete sample |
| `/v1/voices/{voice_id}/samples/{sample_id}/audio` | GET | Download sample |

## Examples

### List All Voices
```bash
curl "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: YOUR_API_KEY" | jq '.voices[] | {name, voice_id, category}'
```

### Python: List Voices
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

voices = client.voices.get_all()
for voice in voices.voices:
    print(f"{voice.name}: {voice.voice_id} ({voice.category})")
```

### Search Voice Library
```python
# Search shared voices with filters
shared = client.voices.get_shared(
    page_size=20,
    gender="female",
    language="en",
    accent="american",
    age="young",
    category="professional"
)

for voice in shared.voices:
    print(f"{voice.name}: {voice.voice_id}")
    print(f"  Preview: {voice.preview_url}")
```

### Clone Voice from Audio
```python
# Clone from audio files (Instant Voice Cloning)
with open("sample1.mp3", "rb") as f1, open("sample2.mp3", "rb") as f2:
    voice = client.voices.add(
        name="My Cloned Voice",
        description="Cloned from recordings",
        files=[f1, f2],
        labels={"accent": "american", "gender": "male"}
    )
    print(f"Created voice: {voice.voice_id}")
```

### Design Synthetic Voice
```python
# Generate a completely new synthetic voice
params = client.voice_generation.get_parameters()

voice = client.voice_generation.generate(
    gender="female",
    age="young",
    accent="american",
    accent_strength=1.0,
    text="Hi there! This is a sample of my voice. I hope you like how I sound!"
)

# Save the generated voice
saved = client.voices.add(
    name="Designed Voice",
    generated_voice_id=voice.generated_voice_id
)
```

### Get Voice Details
```python
voice = client.voices.get("EXAVITQu4vr4xnSDxMaL")
print(f"Name: {voice.name}")
print(f"Category: {voice.category}")
print(f"Labels: {voice.labels}")
print(f"Settings: {voice.settings}")
```

### Update Voice Settings
```python
client.voices.edit_settings(
    voice_id="your_voice_id",
    settings={
        "stability": 0.6,
        "similarity_boost": 0.8,
        "style": 0.2,
        "use_speaker_boost": True
    }
)
```

### Delete Voice
```python
client.voices.delete("voice_id_to_delete")
```

## Voice Categories

| Category | Description |
|----------|-------------|
| `premade` | ElevenLabs built-in voices |
| `cloned` | User-cloned voices |
| `generated` | AI-designed voices |
| `professional` | Premium library voices |

## Voice Settings Reference

| Setting | Range | Description |
|---------|-------|-------------|
| `stability` | 0.0-1.0 | Consistency vs expressiveness |
| `similarity_boost` | 0.0-1.0 | Closeness to original voice |
| `style` | 0.0-1.0 | Style exaggeration (v2+ only) |
| `use_speaker_boost` | boolean | Enhance clarity |

## Library Search Filters

| Filter | Type | Options |
|--------|------|---------|
| `gender` | string | male, female, neutral |
| `age` | string | young, middle_aged, old |
| `accent` | string | american, british, australian, etc. |
| `language` | string | en, es, fr, de, etc. |
| `use_case` | string | narration, conversational, characters |
| `category` | string | professional, generated, cloned |

## Pre-made Voice IDs

### Female Voices
| Name | Voice ID | Accent | Style |
|------|----------|--------|-------|
| Sarah | `EXAVITQu4vr4xnSDxMaL` | American | Soft, friendly |
| Rachel | `21m00Tcm4TlvDq8ikWAM` | American | Calm, professional |
| Emily | `LcfcDJNUP1GQjkzn1xUU` | American | Warm, conversational |
| Elli | `MF3mGyEYCl7XYWbV9V6O` | American | Young, energetic |
| Charlotte | `XB0fDUnXU5powFXDhCwa` | British | Warm, articulate |

### Male Voices
| Name | Voice ID | Accent | Style |
|------|----------|--------|-------|
| Adam | `pNInz6obpgDQGcFmaJgB` | American | Deep, authoritative |
| Antoni | `ErXwobaYiN019PkySvjV` | American | Warm, conversational |
| Josh | `TxGEqnHWrfWFTfGW9XjX` | American | Young, energetic |
| Arnold | `VR6AewLTigWG4xSOukaG` | American | Confident, bold |
| Sam | `yoZ06aMxZJJ28mfd3POQ` | American | Raspy, authentic |
| Daniel | `onwK4e9ZLuTAKqWW03F9` | British | Deep, authoritative |

## Voice Cloning Tips

### Audio Quality Requirements
- **Format**: MP3, WAV, M4A
- **Length**: 1-5 minutes total (multiple samples OK)
- **Quality**: Clean audio, minimal background noise
- **Content**: Natural speech, varied intonation

### Best Practices
1. Use multiple samples (3-5 recommended)
2. Include varied emotional tones
3. Avoid music or sound effects
4. Record in quiet environment
5. Use consistent microphone distance

## Quotas by Tier

| Tier | Custom Voices | Cloned Voices |
|------|---------------|---------------|
| Free | 3 | 0 |
| Starter | 10 | 3 |
| Creator | 30 | 10 |
| Pro | 100 | 30 |
| Scale | Unlimited | 100 |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid API key | Check credentials |
| 404 | Voice not found | Verify voice_id |
| 422 | Invalid audio | Check file format/quality |
| 403 | Voice quota exceeded | Upgrade plan or delete voices |
