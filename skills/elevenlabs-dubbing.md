---
name: elevenlabs-dubbing
description: "Dub videos and audio into multiple languages using ElevenLabs Dubbing API. Automatic speaker detection, transcript generation, and voice cloning."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Dubbing Skill

Automatically translate and dub audio/video content into multiple languages while preserving speaker voices, emotion, and timing.

## Related Skills
- `elevenlabs-stt` - For transcription-only use cases
- `elevenlabs-voices` - Customize voice selection
- `elevenlabs-tts` - For single-voice narration

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/dubbing` | POST | Create dubbing project |
| `/v1/dubbing/{dubbing_id}` | GET | Get dubbing status |
| `/v1/dubbing/{dubbing_id}` | DELETE | Delete dubbing project |
| `/v1/dubbing/{dubbing_id}/audio/{lang}` | GET | Download dubbed audio |
| `/v1/dubbing/{dubbing_id}/transcript/{lang}` | GET | Get transcript |

## Features

- **Multi-language**: Dub into 29+ languages
- **Speaker Detection**: Automatically detect multiple speakers
- **Voice Preservation**: Clone and preserve original voices
- **Timing Sync**: Match dubbed audio to original timing
- **Transcript Export**: Get transcripts in any language

## Examples

### Create Dubbing Project (cURL)
```bash
curl -X POST "https://api.elevenlabs.io/v1/dubbing" \
  -H "xi-api-key: YOUR_API_KEY" \
  -F "file=@video.mp4" \
  -F "source_lang=en" \
  -F "target_langs=es,fr,de"
```

### Python: Full Dubbing Workflow
```python
from elevenlabs import ElevenLabs
import time

client = ElevenLabs(api_key="YOUR_API_KEY")

# 1. Create dubbing project
with open("video.mp4", "rb") as video_file:
    dubbing = client.dubbing.create(
        file=video_file,
        source_lang="en",
        target_langs=["es", "fr", "de"],
        name="Marketing Video Dub"
    )

dubbing_id = dubbing.dubbing_id
print(f"Created dubbing project: {dubbing_id}")

# 2. Wait for processing
while True:
    status = client.dubbing.get(dubbing_id)
    print(f"Status: {status.status}")
    
    if status.status == "completed":
        break
    elif status.status == "failed":
        raise Exception(f"Dubbing failed: {status.error}")
    
    time.sleep(30)  # Check every 30 seconds

# 3. Download dubbed audio for each language
for lang in ["es", "fr", "de"]:
    audio = client.dubbing.get_audio(
        dubbing_id=dubbing_id,
        language_code=lang
    )
    
    with open(f"dubbed_{lang}.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)
    print(f"Downloaded: dubbed_{lang}.mp3")

# 4. Get transcripts
for lang in ["en", "es", "fr", "de"]:
    transcript = client.dubbing.get_transcript(
        dubbing_id=dubbing_id,
        language_code=lang
    )
    print(f"\n{lang.upper()} Transcript:\n{transcript.text}")
```

### Dub from URL
```python
# Dub directly from a video URL
dubbing = client.dubbing.create(
    source_url="https://example.com/video.mp4",
    source_lang="en",
    target_langs=["ja", "ko", "zh"]
)
```

### Customize Speaker Voices
```python
# Get dubbing with speaker info
dubbing = client.dubbing.get(dubbing_id)

# View detected speakers
for speaker_id, speaker in dubbing.speaker_tracks.items():
    print(f"Speaker {speaker_id}: {speaker.speaker_name}")
    print(f"  Segments: {len(speaker.segments)}")
    
# Assign custom voices to speakers (via dashboard or API)
```

### Node.js Example
```javascript
const { ElevenLabsClient } = require("@elevenlabs/elevenlabs-js");
const fs = require("fs");

const client = new ElevenLabsClient({ apiKey: "YOUR_API_KEY" });

async function dubVideo() {
    // Create dubbing project
    const dubbing = await client.dubbing.create({
        file: fs.createReadStream("video.mp4"),
        source_lang: "en",
        target_langs: ["es", "fr"]
    });
    
    console.log("Dubbing ID:", dubbing.dubbing_id);
    
    // Poll for completion
    let status;
    do {
        await new Promise(r => setTimeout(r, 30000));
        status = await client.dubbing.get(dubbing.dubbing_id);
        console.log("Status:", status.status);
    } while (status.status === "processing");
    
    // Download Spanish dub
    const audio = await client.dubbing.getAudio({
        dubbing_id: dubbing.dubbing_id,
        language_code: "es"
    });
    
    fs.writeFileSync("dubbed_es.mp3", Buffer.from(audio));
}

dubVideo();
```

## Supported Languages

### Source Languages
Any of the 29+ ElevenLabs supported languages

### Target Languages
| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `ja` | Japanese |
| `es` | Spanish | `ko` | Korean |
| `fr` | French | `zh` | Chinese |
| `de` | German | `ar` | Arabic |
| `it` | Italian | `hi` | Hindi |
| `pt` | Portuguese | `ru` | Russian |
| `pl` | Polish | `nl` | Dutch |
| `sv` | Swedish | `tr` | Turkish |

## Dubbing Status Values

| Status | Description |
|--------|-------------|
| `pending` | Project created, waiting to start |
| `processing` | Dubbing in progress |
| `completed` | Dubbing finished successfully |
| `failed` | Dubbing failed (check error message) |

## Response Format

### Dubbing Project
```json
{
    "dubbing_id": "dub_abc123",
    "name": "My Video",
    "status": "completed",
    "source_language": "en",
    "target_languages": ["es", "fr"],
    "speaker_tracks": {
        "speaker_1": {
            "id": "speaker_1",
            "speaker_name": "Speaker 1",
            "segments": ["seg_1", "seg_2"]
        }
    },
    "renders": {
        "es": {
            "status": "complete",
            "media_ref": {...}
        }
    }
}
```

## Best Practices

### Input Quality
1. **Clear Audio**: Remove background music/noise when possible
2. **Speaker Separation**: Ensure speakers don't overlap
3. **Video Format**: MP4 with AAC audio works best
4. **Resolution**: Higher quality = better lip sync

### Project Management
1. **Naming**: Use descriptive names for projects
2. **Batch Processing**: Group related videos
3. **Cost Management**: Preview before full dub

### Quality Assurance
1. **Review Transcripts**: Check source transcript accuracy
2. **Speaker Assignment**: Verify speaker detection
3. **Voice Matching**: Assign appropriate voices

## Pricing Considerations

| Factor | Impact |
|--------|--------|
| Duration | Primary cost driver |
| Languages | Each target language billed separately |
| Speakers | More speakers may affect quality |
| Resolution | Video quality doesn't affect cost |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid file format | Use MP4, MP3, WAV |
| 401 | Invalid API key | Check credentials |
| 413 | File too large | Compress or split video |
| 422 | Unsupported language | Check language codes |
| 500 | Processing error | Retry or contact support |

## Use Cases

### Corporate Training
```python
# Dub training videos into regional languages
dubbing = client.dubbing.create(
    file=training_video,
    source_lang="en",
    target_langs=["es-MX", "pt-BR", "fr-CA"],  # Regional variants
    name="Safety Training Q1 2024"
)
```

### YouTube Localization
```python
# Create multilingual versions of content
dubbing = client.dubbing.create(
    source_url=youtube_url,
    source_lang="en",
    target_langs=["es", "pt", "de", "fr", "ja", "ko"],
    name="Product Launch Video"
)
```

### Podcast Translation
```python
# Dub podcast episodes
dubbing = client.dubbing.create(
    file=podcast_episode,
    source_lang="en",
    target_langs=["es"],
    name="Podcast Ep 42 - Spanish"
)

# Get audio-only output
spanish_audio = client.dubbing.get_audio(
    dubbing_id=dubbing.dubbing_id,
    language_code="es"
)
```
