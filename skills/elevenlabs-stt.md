---
name: elevenlabs-stt
description: "Transcribe audio to text using ElevenLabs Speech-to-Text API. Supports file upload and real-time WebSocket streaming with multiple languages."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Speech-to-Text Skill

Transcribe audio files or real-time audio streams to text with high accuracy and multi-language support.

## Related Skills
- `elevenlabs-tts` - Convert text back to speech
- `elevenlabs-dubbing` - Transcribe and dub videos
- `elevenlabs-audio-tools` - Clean audio before transcription

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/speech-to-text` | POST | Transcribe audio file |
| `/v1/speech-to-text/realtime` | WebSocket | Real-time streaming |

## Supported Languages

ElevenLabs STT supports 29+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese, Japanese, Korean
- Arabic, Hindi, Russian
- Dutch, Polish, Swedish, Norwegian, Danish, Finnish
- And more...

## Examples

### Transcribe Audio File (cURL)
```bash
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: YOUR_API_KEY" \
  -F "audio=@recording.mp3" \
  -F "model_id=scribe_v1" \
  -F "language_code=en"
```

### Python: Transcribe File
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

with open("audio.mp3", "rb") as audio_file:
    result = client.speech_to_text.convert(
        audio=audio_file,
        model_id="scribe_v1",
        language_code="en"  # Optional: auto-detect if omitted
    )
    
print(f"Transcription: {result.text}")
print(f"Detected language: {result.language_code}")
```

### Transcription with Timestamps
```python
result = client.speech_to_text.convert(
    audio=audio_file,
    model_id="scribe_v1",
    timestamps_granularity="word"  # or "sentence"
)

for word in result.words:
    print(f"{word.text}: {word.start_time}s - {word.end_time}s")
```

### Real-time WebSocket Transcription
```python
import asyncio
import websockets
import json
import base64

async def realtime_transcribe():
    uri = "wss://api.elevenlabs.io/v1/speech-to-text/realtime"
    
    async with websockets.connect(
        uri,
        extra_headers={"xi-api-key": "YOUR_API_KEY"}
    ) as ws:
        # Send configuration
        await ws.send(json.dumps({
            "type": "config",
            "model_id": "scribe_v1",
            "language_code": "en",
            "sample_rate": 16000
        }))
        
        # Stream audio chunks
        async def send_audio():
            with open("audio.raw", "rb") as f:
                while chunk := f.read(4096):
                    await ws.send(json.dumps({
                        "type": "audio",
                        "audio": base64.b64encode(chunk).decode()
                    }))
                    await asyncio.sleep(0.1)
            
            # Signal end of audio
            await ws.send(json.dumps({"type": "end"}))
        
        # Receive transcriptions
        async def receive_transcripts():
            async for message in ws:
                data = json.loads(message)
                if data["type"] == "transcript":
                    print(f"Transcript: {data['text']}")
                    if data.get("is_final"):
                        print("--- Final ---")
        
        await asyncio.gather(send_audio(), receive_transcripts())

asyncio.run(realtime_transcribe())
```

### Node.js: Transcribe File
```javascript
const { ElevenLabsClient } = require("@elevenlabs/elevenlabs-js");
const fs = require("fs");

const client = new ElevenLabsClient({ apiKey: "YOUR_API_KEY" });

async function transcribe() {
    const audio = fs.createReadStream("recording.mp3");
    
    const result = await client.speechToText.convert({
        audio: audio,
        model_id: "scribe_v1"
    });
    
    console.log("Transcription:", result.text);
}

transcribe();
```

## Audio Format Requirements

| Parameter | Requirement |
|-----------|-------------|
| **Formats** | MP3, WAV, M4A, FLAC, OGG, WebM |
| **Max file size** | 25 MB |
| **Max duration** | 2 hours |
| **Sample rate** | 8kHz - 48kHz |
| **Channels** | Mono or Stereo |

### For WebSocket Streaming
| Parameter | Requirement |
|-----------|-------------|
| **Format** | PCM 16-bit signed little-endian |
| **Sample rate** | 16000 Hz recommended |
| **Channels** | Mono |

## Response Format

```json
{
    "text": "Hello, this is the transcribed text.",
    "language_code": "en",
    "language_probability": 0.98,
    "words": [
        {
            "text": "Hello",
            "start_time": 0.0,
            "end_time": 0.5,
            "confidence": 0.99
        },
        {
            "text": "this",
            "start_time": 0.6,
            "end_time": 0.8,
            "confidence": 0.97
        }
    ]
}
```

## WebSocket Events

### Client → Server
| Event | Description |
|-------|-------------|
| `config` | Initial configuration (model, language, sample_rate) |
| `audio` | Base64-encoded audio chunk |
| `end` | Signal end of audio stream |

### Server → Client
| Event | Description |
|-------|-------------|
| `transcript` | Partial or final transcription |
| `error` | Error message |
| `end` | Transcription complete |

## Use Cases

### Meeting Transcription
```python
def transcribe_meeting(audio_path):
    with open(audio_path, "rb") as f:
        result = client.speech_to_text.convert(
            audio=f,
            model_id="scribe_v1",
            timestamps_granularity="sentence"
        )
    
    # Format as meeting notes
    notes = []
    for sentence in result.sentences:
        timestamp = f"[{sentence.start_time:.1f}s]"
        notes.append(f"{timestamp} {sentence.text}")
    
    return "\n".join(notes)
```

### Subtitle Generation
```python
def generate_srt(audio_path):
    with open(audio_path, "rb") as f:
        result = client.speech_to_text.convert(
            audio=f,
            timestamps_granularity="word"
        )
    
    # Generate SRT format
    srt_lines = []
    for i, word in enumerate(result.words):
        start = format_srt_time(word.start_time)
        end = format_srt_time(word.end_time)
        srt_lines.append(f"{i+1}\n{start} --> {end}\n{word.text}\n")
    
    return "\n".join(srt_lines)

def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

### Live Captioning
```python
import pyaudio
import asyncio

async def live_caption():
    # Initialize microphone
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    uri = "wss://api.elevenlabs.io/v1/speech-to-text/realtime"
    
    async with websockets.connect(uri, extra_headers={"xi-api-key": KEY}) as ws:
        await ws.send(json.dumps({
            "type": "config",
            "model_id": "scribe_v1",
            "sample_rate": 16000
        }))
        
        while True:
            audio_data = stream.read(1024)
            await ws.send(json.dumps({
                "type": "audio",
                "audio": base64.b64encode(audio_data).decode()
            }))
            
            # Check for transcripts
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.01)
                data = json.loads(msg)
                if data["type"] == "transcript":
                    print(data["text"], end=" ", flush=True)
            except asyncio.TimeoutError:
                pass
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid audio format | Convert to supported format |
| 401 | Invalid API key | Check credentials |
| 413 | File too large | Split into smaller chunks |
| 422 | Unsupported language | Use supported language code |
| 429 | Rate limit | Implement backoff |

## Best Practices

1. **Audio Quality**: Clean audio produces better transcripts
2. **Language Hint**: Provide `language_code` when known for better accuracy
3. **Chunking**: For long files, consider splitting at natural breaks
4. **WebSocket**: Use for real-time; REST for batch processing
5. **Error Handling**: Always handle network interruptions for WebSocket
