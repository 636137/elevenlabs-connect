---
name: elevenlabs-tts
description: "Generate speech from text using ElevenLabs Text-to-Speech and Speech-to-Speech APIs. Supports streaming, timestamps, voice settings, and pronunciation dictionaries."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Text-to-Speech Skill

Generate high-quality speech from text using ElevenLabs' industry-leading TTS models.

## Related Skills
- `elevenlabs-voices` - Manage voices (required for voice_id selection)
- `elevenlabs-admin` - Check usage/subscription limits
- `elevenlabs-convai-agents` - For conversational AI agents

## API Endpoints

### Text-to-Speech
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/text-to-speech/{voice_id}` | POST | Convert text to speech |
| `/v1/text-to-speech/{voice_id}/stream` | POST | Stream audio in chunks |
| `/v1/text-to-speech/{voice_id}/with-timestamps` | POST | Get word-level timestamps |

### Speech-to-Speech (Voice Conversion)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/speech-to-speech/{voice_id}` | POST | Convert audio to another voice |
| `/v1/speech-to-speech/{voice_id}/stream` | POST | Stream voice conversion |

## Available Models

| Model ID | Description | Best For |
|----------|-------------|----------|
| `eleven_v3` | Latest flagship model | Highest quality |
| `eleven_multilingual_v2` | 29 languages | International content |
| `eleven_flash_v2_5` | Ultra-low latency | Real-time apps |
| `eleven_turbo_v2_5` | Fast generation | Production workloads |
| `eleven_turbo_v2` | Legacy turbo | Backward compatibility |
| `eleven_english_sts_v2` | Speech-to-speech | Voice conversion |

## Output Formats

| Format | Sample Rate | Bitrate | Notes |
|--------|-------------|---------|-------|
| `mp3_44100_128` | 44.1kHz | 128kbps | Default, good quality |
| `mp3_44100_192` | 44.1kHz | 192kbps | Creator tier+ |
| `pcm_16000` | 16kHz | PCM | Telephony (Twilio) |
| `pcm_22050` | 22.05kHz | PCM | Standard PCM |
| `pcm_44100` | 44.1kHz | PCM | Pro tier+ |
| `ulaw_8000` | 8kHz | μ-law | Twilio compatible |

## Examples

### Basic Text-to-Speech
```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}" \
  -H "xi-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of ElevenLabs text to speech.",
    "model_id": "eleven_turbo_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "use_speaker_boost": true
    }
  }' \
  --output speech.mp3
```

### Python SDK
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Generate speech
audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah
    text="Hello world!",
    model_id="eleven_turbo_v2",
    output_format="mp3_44100_128"
)

# Save to file
with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Streaming TTS
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Stream audio chunks
for chunk in client.text_to_speech.convert_as_stream(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    text="This is streaming audio generation.",
    model_id="eleven_flash_v2_5"
):
    # Process each chunk (e.g., play or send to client)
    process_audio_chunk(chunk)
```

### TTS with Timestamps
```python
response = client.text_to_speech.convert_with_timestamps(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    text="Hello world, this is a test.",
    model_id="eleven_turbo_v2"
)

# Access word-level timing
for alignment in response.alignment:
    print(f"Word: {alignment.word}, Start: {alignment.start_time}s, End: {alignment.end_time}s")
```

### Speech-to-Speech (Voice Conversion)
```python
# Convert your voice to another voice
with open("input_audio.mp3", "rb") as audio_file:
    converted = client.speech_to_speech.convert(
        voice_id="TARGET_VOICE_ID",
        audio=audio_file,
        model_id="eleven_english_sts_v2",
        remove_background_noise=True
    )
```

## Voice Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| `stability` | 0.0-1.0 | 0.5 | Higher = more consistent, lower = more expressive |
| `similarity_boost` | 0.0-1.0 | 0.75 | Higher = closer to original voice |
| `style` | 0.0-1.0 | 0.0 | Exaggeration of voice style (v2+ models) |
| `use_speaker_boost` | bool | true | Enhance voice clarity |

### Recommended Settings by Use Case

| Use Case | Stability | Similarity | Style |
|----------|-----------|------------|-------|
| Audiobooks | 0.7 | 0.5 | 0.0 |
| News/Narration | 0.8 | 0.7 | 0.0 |
| Conversational | 0.5 | 0.75 | 0.3 |
| Character Voices | 0.3 | 0.8 | 0.5 |
| Podcast | 0.6 | 0.6 | 0.2 |

## Pronunciation Dictionaries

Control pronunciation of specific words:

```python
# Add pronunciation rules
audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    text="Welcome to the AWS re:Invent conference.",
    pronunciation_dictionary_locators=[
        {
            "pronunciation_dictionary_id": "dict_id",
            "version_id": "version_id"
        }
    ]
)
```

## Request Stitching (Continuity)

For long content split across requests:

```python
# First segment
response1 = client.text_to_speech.convert(
    voice_id="voice_id",
    text="This is the first part of a long text.",
    next_text="This is the second part."  # Hint for continuity
)

# Second segment
response2 = client.text_to_speech.convert(
    voice_id="voice_id",
    text="This is the second part.",
    previous_request_ids=[response1.request_id]  # Link to previous
)
```

## Common Voice IDs (Pre-made)

| Name | Voice ID | Description |
|------|----------|-------------|
| Sarah | `EXAVITQu4vr4xnSDxMaL` | Soft, friendly female |
| Rachel | `21m00Tcm4TlvDq8ikWAM` | Calm, professional female |
| Adam | `pNInz6obpgDQGcFmaJgB` | Deep, authoritative male |
| Antoni | `ErXwobaYiN019PkySvjV` | Warm, conversational male |
| Josh | `TxGEqnHWrfWFTfGW9XjX` | Young, energetic male |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid API key | Check `xi-api-key` header |
| 422 | Invalid voice_id | Use `elevenlabs-voices` skill to list valid IDs |
| 429 | Rate limit exceeded | Implement backoff, check subscription |
| 400 | Text too long | Split text into smaller chunks |

## Character Limits

| Tier | Max chars/request |
|------|-------------------|
| Free | 2,500 |
| Starter | 5,000 |
| Creator | 5,000 |
| Pro | 10,000 |
| Scale | 10,000 |

## Cost Tracking

Access character cost from response headers:
```python
response = client.text_to_speech.with_raw_response.convert(...)
char_cost = response.headers.get("x-character-count")
request_id = response.headers.get("request-id")
```
