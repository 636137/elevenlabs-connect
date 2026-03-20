# GitHub Copilot Skills

This directory contains GitHub Copilot skills for AI-assisted development with ElevenLabs and web UI creation.

## Installation

Copy the skills you want to your Copilot skills directory:

```bash
# macOS/Linux
mkdir -p ~/.copilot/skills

# Install a single skill
mkdir -p ~/.copilot/skills/elevenlabs-convai-agents
cp elevenlabs-convai-agents.md ~/.copilot/skills/elevenlabs-convai-agents/SKILL.md

# Or install all skills
for skill in *.md; do
    name="${skill%.md}"
    if [ "$name" != "README" ]; then
        mkdir -p ~/.copilot/skills/$name
        cp "$skill" ~/.copilot/skills/$name/SKILL.md
        echo "Installed $name"
    fi
done
```

## Available Skills

### ElevenLabs Conversational AI

| Skill | Description |
|-------|-------------|
| `elevenlabs-convai-agents` | Build and embed voice AI agents with working audio |
| `connect-elevenlabs-setup` | Set up ElevenLabs with Amazon Connect (Secrets Manager, KMS) |

### ElevenLabs Audio Suite

| Skill | Description |
|-------|-------------|
| `elevenlabs-tts` | Text-to-Speech and Speech-to-Speech synthesis |
| `elevenlabs-voices` | Voice management, cloning, and design |
| `elevenlabs-stt` | Speech-to-Text transcription |
| `elevenlabs-dubbing` | Video and audio dubbing |
| `elevenlabs-audio-tools` | Sound effects, noise removal, audio players |
| `elevenlabs-projects` | Long-form audiobooks and podcasts |
| `elevenlabs-admin` | Account management, usage, history, models |

### UI Development

| Skill | Description |
|-------|-------------|
| `frontend-design` | Create distinctive, production-grade frontend interfaces |
| `web-artifacts-builder` | Build complex React/Tailwind/shadcn applications |

## Usage

After installing, invoke skills in GitHub Copilot:

```
Use the elevenlabs-convai-agents skill to create a customer support agent
```

```
Use the frontend-design skill to create a landing page for my AI agent
```

## UI Design Guidelines

When building web interfaces:

**Do:**
- Use proper icons (SVG, Heroicons, Lucide)
- Choose distinctive fonts
- Create unique color schemes

**Don't:**
- Never use emojis in the UI
- Avoid purple gradients on white
- Don't use cookie-cutter layouts
