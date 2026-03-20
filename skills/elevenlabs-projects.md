---
name: elevenlabs-projects
description: "Create and manage long-form audio content with ElevenLabs Projects (Studio). Build audiobooks, podcasts, and multi-chapter content with consistent voice and quality."
user-invocable: true
disable-model-invocation: false
---

# ElevenLabs Projects Skill

Create long-form audio content like audiobooks, podcasts, and training materials using ElevenLabs Projects (formerly Studio). Manage chapters, maintain voice consistency, and convert large documents to audio.

## Related Skills
- `elevenlabs-tts` - Single-request TTS
- `elevenlabs-voices` - Voice selection and settings
- `elevenlabs-admin` - Usage and quota management

## API Endpoints

### Projects
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/projects` | GET | List all projects |
| `/v1/projects/add` | POST | Create new project |
| `/v1/projects/{project_id}` | GET | Get project details |
| `/v1/projects/{project_id}` | DELETE | Delete project |
| `/v1/projects/{project_id}/convert` | POST | Convert project to audio |
| `/v1/projects/{project_id}/snapshots` | GET | List project versions |

### Chapters
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/projects/{project_id}/chapters` | GET | List chapters |
| `/v1/projects/{project_id}/chapters/add` | POST | Add chapter |
| `/v1/projects/{project_id}/chapters/{chapter_id}` | GET | Get chapter |
| `/v1/projects/{project_id}/chapters/{chapter_id}` | DELETE | Delete chapter |
| `/v1/projects/{project_id}/chapters/{chapter_id}/convert` | POST | Convert chapter |

## Examples

### Create Project from Text
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Create a new project
project = client.projects.add(
    name="My Audiobook",
    default_title_voice_id="EXAVITQu4vr4xnSDxMaL",
    default_paragraph_voice_id="EXAVITQu4vr4xnSDxMaL",
    default_model_id="eleven_turbo_v2",
    from_document=open("book.txt", "rb")
)

print(f"Created project: {project.project_id}")
```

### Create Project with Chapters
```python
# Create empty project
project = client.projects.add(
    name="Training Course",
    default_title_voice_id="voice_id",
    default_paragraph_voice_id="voice_id",
    default_model_id="eleven_turbo_v2"
)

# Add chapters
chapters = [
    ("Introduction", "Welcome to this training course..."),
    ("Module 1", "In this first module, we will cover..."),
    ("Module 2", "Building on what we learned..."),
    ("Conclusion", "Thank you for completing this course...")
]

for title, content in chapters:
    chapter = client.projects.chapters.add(
        project_id=project.project_id,
        name=title,
        from_text=content
    )
    print(f"Added chapter: {chapter.chapter_id}")
```

### List Projects
```python
projects = client.projects.get_all()

for project in projects.projects:
    print(f"{project.name} ({project.project_id})")
    print(f"  State: {project.state}")
    print(f"  Chapters: {project.chapter_count}")
```

### Get Project Details
```python
project = client.projects.get("project_id")

print(f"Name: {project.name}")
print(f"State: {project.state}")
print(f"Created: {project.created_at}")
print(f"Default Voice: {project.default_paragraph_voice_id}")
print(f"Default Model: {project.default_model_id}")
```

### Convert Project to Audio
```python
# Start conversion
conversion = client.projects.convert(
    project_id=project.project_id
)

# Poll for completion
import time
while True:
    project = client.projects.get(project.project_id)
    print(f"State: {project.state}")
    
    if project.state == "completed":
        break
    elif project.state == "failed":
        raise Exception("Conversion failed")
    
    time.sleep(10)

# Get snapshots (converted versions)
snapshots = client.projects.get_snapshots(project.project_id)
latest = snapshots.snapshots[0]

# Download audio
print(f"Download URL: {latest.audio_url}")
```

### Work with Chapters
```python
# List chapters
chapters = client.projects.chapters.get_all(project.project_id)

for chapter in chapters.chapters:
    print(f"Chapter: {chapter.name}")
    print(f"  State: {chapter.state}")
    print(f"  Conversion Progress: {chapter.conversion_progress}")

# Get specific chapter
chapter = client.projects.chapters.get(
    project_id=project.project_id,
    chapter_id="chapter_id"
)

# Convert single chapter
client.projects.chapters.convert(
    project_id=project.project_id,
    chapter_id="chapter_id"
)

# Delete chapter
client.projects.chapters.delete(
    project_id=project.project_id,
    chapter_id="chapter_id"
)
```

### Upload Document Formats
```python
# Support for various formats
# EPUB (books)
project = client.projects.add(
    name="Ebook Audiobook",
    default_title_voice_id="voice_id",
    default_paragraph_voice_id="voice_id",
    from_document=open("book.epub", "rb")
)

# PDF
project = client.projects.add(
    name="PDF to Audio",
    default_title_voice_id="voice_id",
    default_paragraph_voice_id="voice_id",
    from_document=open("document.pdf", "rb")
)

# HTML
project = client.projects.add(
    name="Web Article",
    default_title_voice_id="voice_id",
    default_paragraph_voice_id="voice_id",
    from_document=open("article.html", "rb")
)
```

### Create from URL
```python
# Create project from web URL
project = client.projects.add(
    name="Blog Post Audio",
    default_title_voice_id="voice_id",
    default_paragraph_voice_id="voice_id",
    from_url="https://example.com/blog-post"
)
```

## Project States

| State | Description |
|-------|-------------|
| `created` | Project created, not yet converted |
| `converting` | Conversion in progress |
| `completed` | Conversion successful |
| `failed` | Conversion failed |

## Supported Document Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Plain Text | .txt | Best for clean content |
| EPUB | .epub | Automatic chapter detection |
| PDF | .pdf | May need manual cleanup |
| HTML | .html | Strips formatting |
| DOCX | .docx | Microsoft Word |
| Markdown | .md | Common for tech content |

## Best Practices

### Content Preparation
1. **Clean Text**: Remove headers, footers, page numbers
2. **Chapter Markers**: Use consistent heading levels
3. **Abbreviations**: Spell out or use pronunciation hints
4. **Numbers**: Write as words when natural ("two hundred" vs "200")

### Voice Consistency
1. Use same voice_id across chapters
2. Set default model at project level
3. Preview before full conversion

### Large Documents
1. Split very large books into multiple projects
2. Convert chapters individually for testing
3. Use snapshots to track versions

## Character Limits

| Tier | Max chars/project |
|------|-------------------|
| Starter | 50,000 |
| Creator | 250,000 |
| Pro | 1,000,000 |
| Scale | Unlimited |

## Example: Full Audiobook Workflow

```python
from elevenlabs import ElevenLabs
import time

client = ElevenLabs(api_key="YOUR_API_KEY")

def create_audiobook(epub_path, voice_id, name):
    """Convert an EPUB to audiobook."""
    
    # 1. Create project from EPUB
    with open(epub_path, "rb") as f:
        project = client.projects.add(
            name=name,
            default_title_voice_id=voice_id,
            default_paragraph_voice_id=voice_id,
            default_model_id="eleven_turbo_v2",
            from_document=f
        )
    
    print(f"Created project: {project.project_id}")
    
    # 2. List auto-detected chapters
    chapters = client.projects.chapters.get_all(project.project_id)
    print(f"Found {len(chapters.chapters)} chapters")
    
    for ch in chapters.chapters:
        print(f"  - {ch.name}")
    
    # 3. Convert entire project
    print("Starting conversion...")
    client.projects.convert(project.project_id)
    
    # 4. Wait for completion
    while True:
        proj = client.projects.get(project.project_id)
        print(f"State: {proj.state}")
        
        if proj.state == "completed":
            break
        elif proj.state == "failed":
            raise Exception("Conversion failed")
        
        time.sleep(30)
    
    # 5. Get download URL
    snapshots = client.projects.get_snapshots(project.project_id)
    if snapshots.snapshots:
        print(f"Download: {snapshots.snapshots[0].audio_url}")
        return snapshots.snapshots[0].audio_url
    
    return None

# Usage
audio_url = create_audiobook(
    epub_path="my_book.epub",
    voice_id="EXAVITQu4vr4xnSDxMaL",
    name="My Book - Audiobook"
)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid document format | Use supported format |
| 401 | Invalid API key | Check credentials |
| 403 | Quota exceeded | Upgrade plan |
| 413 | Document too large | Split into smaller parts |
| 422 | Conversion error | Check document content |
