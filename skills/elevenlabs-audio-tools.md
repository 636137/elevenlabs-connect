---
name: elevenlabs-audio-tools
description: "Audio processing utilities: noise removal (audio isolation), AI sound effects generation, and Audio Native embedded players."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Audio Tools Skill

Audio processing utilities including background noise removal, AI-generated sound effects, and embeddable audio players for websites.

## Related Skills
- `elevenlabs-tts` - Generate speech audio
- `elevenlabs-stt` - Transcribe cleaned audio
- `elevenlabs-dubbing` - Full video dubbing

## API Endpoints

### Audio Isolation (Noise Removal)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/audio-isolation` | POST | Remove background noise |
| `/v1/audio-isolation/stream` | POST | Stream cleaned audio |

### Sound Generation
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/sound-generation` | POST | Generate sound effects from text |

### Audio Native (Embedded Players)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/audio-native` | POST | Create embeddable audio project |
| `/v1/audio-native/{project_id}` | GET | Get project details |

---

## Audio Isolation (Noise Removal)

Remove background noise, music, and ambient sounds from audio, isolating vocals/speech.

### Basic Usage (cURL)
```bash
curl -X POST "https://api.elevenlabs.io/v1/audio-isolation" \
  -H "xi-api-key: YOUR_API_KEY" \
  -F "audio=@noisy_audio.mp3" \
  --output clean_audio.mp3
```

### Python: Clean Audio File
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

with open("noisy_recording.mp3", "rb") as audio:
    cleaned = client.audio_isolation.convert(audio=audio)

with open("cleaned_audio.mp3", "wb") as f:
    for chunk in cleaned:
        f.write(chunk)

print("Audio cleaned and saved!")
```

### Streaming Audio Isolation
```python
# For real-time processing
with open("noisy_audio.mp3", "rb") as audio:
    for chunk in client.audio_isolation.convert_as_stream(audio=audio):
        # Process each cleaned chunk
        process_chunk(chunk)
```

### Use Cases
- **Podcast Cleanup**: Remove HVAC, traffic, or room noise
- **Meeting Audio**: Clean up Zoom/Teams recordings  
- **Voice Cloning Prep**: Get clean samples for cloning
- **Interview Processing**: Isolate speaker voices

---

## Sound Effects Generation

Generate custom sound effects from text descriptions using AI.

### Basic Usage (cURL)
```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Thunder rumbling in the distance followed by heavy rain",
    "duration_seconds": 10,
    "prompt_influence": 0.5
  }' \
  --output thunder_rain.mp3
```

### Python: Generate Sound Effects
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Generate a sound effect
sound = client.sound_generation.generate(
    text="A door creaking open slowly in a haunted house",
    duration_seconds=5,
    prompt_influence=0.3  # 0.0-1.0, higher = more literal
)

with open("creaky_door.mp3", "wb") as f:
    for chunk in sound:
        f.write(chunk)
```

### Sound Effect Prompts

| Category | Example Prompts |
|----------|-----------------|
| **Nature** | "Ocean waves crashing on a rocky shore" |
| **Weather** | "Gentle rain on a tin roof" |
| **Urban** | "City traffic with honking cars and sirens" |
| **Animals** | "Dog barking excitedly at the door" |
| **Mechanical** | "Old elevator doors opening with a ding" |
| **Sci-Fi** | "Futuristic spaceship engine humming" |
| **Horror** | "Footsteps echoing in an empty hallway" |
| **Action** | "Glass shattering and debris falling" |

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `text` | string | - | Description of the sound |
| `duration_seconds` | float | 0.5-22 | Length of generated audio |
| `prompt_influence` | float | 0.0-1.0 | How literally to follow prompt |

### Tips for Better Results
1. **Be Specific**: "Heavy rain on a metal roof" > "rain"
2. **Add Context**: "In a quiet library" or "During a thunderstorm"
3. **Describe Timing**: "Starting quietly and building to loud"
4. **Multiple Elements**: "Birds chirping with a gentle breeze"

---

## Audio Native (Embedded Players)

Create embeddable audio players for websites that automatically convert text articles to audio.

### Create Audio Native Project
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Create from text
project = client.audio_native.create(
    name="Blog Post Audio",
    title="How to Use ElevenLabs API",
    author="Tech Blog",
    text="Your article content goes here...",
    voice_id="EXAVITQu4vr4xnSDxMaL",
    auto_convert=True
)

print(f"Project ID: {project.project_id}")
print(f"Embed Code:\n{project.html_snippet}")
```

### Create from HTML File
```python
with open("article.html", "rb") as html_file:
    project = client.audio_native.create(
        name="Article Audio",
        file=html_file,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model_id="eleven_turbo_v2",
        auto_convert=True
    )
```

### Embed Code Output
```html
<iframe 
    src="https://elevenlabs.io/player/index.html?publicUserId=xxx&projectId=xxx"
    width="100%" 
    height="200" 
    frameborder="0"
    allow="autoplay">
</iframe>
```

### Customize Player Appearance
```python
project = client.audio_native.create(
    name="Custom Player",
    text="Your content...",
    voice_id="voice_id",
    text_color="#333333",
    background_color="#f5f5f5"
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Project name (required) |
| `title` | string | Display title in player |
| `author` | string | Author name |
| `text` | string | Content to convert |
| `file` | file | HTML/TXT file with content |
| `voice_id` | string | Voice for narration |
| `model_id` | string | TTS model to use |
| `auto_convert` | bool | Start conversion immediately |
| `text_color` | string | Player text color (hex) |
| `background_color` | string | Player background (hex) |

---

## Complete Audio Processing Pipeline

### Clean → Transcribe → Dub
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# 1. Clean noisy audio
with open("raw_interview.mp3", "rb") as raw:
    cleaned = client.audio_isolation.convert(audio=raw)
    
with open("cleaned.mp3", "wb") as f:
    for chunk in cleaned:
        f.write(chunk)

# 2. Transcribe cleaned audio
with open("cleaned.mp3", "rb") as clean:
    transcript = client.speech_to_text.convert(audio=clean)
    print(f"Transcript: {transcript.text}")

# 3. Create TTS from transcript
audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",
    text=transcript.text,
    model_id="eleven_turbo_v2"
)

with open("re-voiced.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Generate Podcast Intro
```python
# Generate intro music sound effect
intro_music = client.sound_generation.generate(
    text="Upbeat podcast intro music with a tech feel, building energy",
    duration_seconds=10
)

# Generate intro narration
intro_voice = client.text_to_speech.convert(
    voice_id="your_voice_id",
    text="Welcome to The Tech Hour, your weekly dive into the latest in technology!",
    model_id="eleven_turbo_v2"
)

# Combine in your audio editor of choice
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid audio format | Use MP3, WAV, M4A |
| 401 | Invalid API key | Check credentials |
| 413 | File too large | Compress audio first |
| 422 | Invalid parameters | Check duration/prompt |
| 429 | Rate limit | Implement backoff |

## Audio Format Support

| Format | Audio Isolation | Sound Gen | Audio Native |
|--------|-----------------|-----------|--------------|
| MP3 | ✅ | ✅ Output | ✅ |
| WAV | ✅ | - | ✅ |
| M4A | ✅ | - | - |
| FLAC | ✅ | - | - |
| OGG | ✅ | - | - |
