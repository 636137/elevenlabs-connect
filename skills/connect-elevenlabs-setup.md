---
name: connect-elevenlabs-setup
description: "Bootstrap Amazon Connect + ElevenLabs TTS: create/update Secrets Manager secret, apply secret+KMS policies safely, and list valid ElevenLabs model IDs + voice IDs filtered by language."
user-invocable: true
disable-model-invocation: false
---

# Amazon Connect + ElevenLabs Setup Skill

Use this skill to reliably configure ElevenLabs as a third-party TTS provider in Amazon Connect **without** re-hitting the common failure modes:

- KMS decrypt denied (`Access to KMS is not allowed`)
- Secret schema mismatch (`secret could not be deserialized`)
- Wrong model string (e.g. `elevenlabs_multilingual_v2` instead of `eleven_multilingual_v2`)

## What this skill does

1. **Secrets Manager**: create/update the ElevenLabs credential secret in the **required JSON schema**.
2. **Secret resource policy**: allow `connect.amazonaws.com` to call `secretsmanager:GetSecretValue` scoped to your instance.
3. **KMS key policy**: allow Connect + Secrets Manager to decrypt **only** for that secret using `kms:EncryptionContext:SecretARN`.
4. **Catalog**: list valid ElevenLabs **model IDs** and **voice IDs**, filtered by language/locale.

## Safety rules (important)

- Never paste API keys into chat, terminals with history, or code repos.
- Prefer using the script's interactive prompt (`--prompt-for-token`) so the token is not echoed.
- If you accidentally exposed a key, revoke/rotate it immediately in ElevenLabs.

## Prerequisites

- AWS credentials available locally (boto3 can call STS/Secrets Manager/KMS).
- Amazon Connect instance ARN.
- A customer-managed KMS key ARN in the **same region** (Secrets Manager cannot use the AWS-managed `aws/secretsmanager` key for this Connect integration).

## Commands

The skill includes a helper script:

- `~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py`

### 1) One-time setup (secret + policies)

```bash
python3 ~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py setup \
  --region us-west-2 \
  --connect-instance-arn arn:aws:connect:us-west-2:ACCOUNT_ID:instance/INSTANCE_ID \
  --secret-name elevenlabs \
  --kms-key-arn arn:aws:kms:us-west-2:ACCOUNT_ID:key/YOUR_KEY_ID \
  --api-token-region us \
  --prompt-for-token \
  --apply --yes
```

### 2) List valid models + voices for a language

```bash
# Example: English (US)
python3 ~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py catalog \
  --region us-west-2 \
  --secret-name elevenlabs \
  --language en-US

# Example: Spanish
python3 ~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py catalog \
  --region us-west-2 \
  --secret-name elevenlabs \
  --language es-US
```

### 3) Render a contact flow JSON from your template export

If you omit `--voice-id`, the script will prompt you to choose a voice **first** (showing up to 10 options).

If you omit `--model-id`, it will then prompt you to choose a model from the **full** ElevenLabs `/v1/models` list available to the API token stored in your AWS secret.

This uses an exported contact flow JSON (like your `/Users/ChadDHendren/Downloads/1 - Elevenlabs Demo 1.json`) as a template and swaps in the selected ElevenLabs model/voice + secret ARN + language + greeting text.

Notes:
- You can pass `--model-id latest` to auto-select the newest model from ElevenLabs `/v1/models`.
- Use `--validate-voice` to confirm the chosen `voice_id` is actually visible to the API token stored in your AWS secret (this is what Amazon Connect will use).

- For long/complex phrases, prefer `--prompt-for-greeting` to paste the phrase interactively (avoids shell quoting/history-expansion issues).

```bash
python3 ~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py flow \
  --template-path "/Users/ChadDHendren/Downloads/1 - Elevenlabs Demo 1.json" \
  --output-path "/Users/ChadDHendren/Downloads/1 - Elevenlabs Demo 1.rendered.json" \
  --region us-west-2 \
  --secret-name elevenlabs \
  --model-id latest \
  --voice-id CwhRBWXzGAHq8TQ4Fs17 \
  --analytics-language en-US \
  --greeting-text "Hi! This is ElevenLabs in Amazon Connect. How can I help?" \
  --ivr-recording enabled \
  --contact-lens enabled
```

### 4) Deploy the flow via APIs (create/update + associate phone number)

`deploy` will:
- Render a new flow from your exported template JSON.
- Create/update (“publish”) the flow via **Amazon Connect APIs**.
- Optionally associate a phone number to the flow.

#### Interactive deploy (voice → model → greeting)

To get the exact interactive experience (this is the preferred path for long/complex phrases):
- **Omit** `--voice-id` to be shown a short list of voice options (up to 10, filtered to your language).
- **Omit** `--model-id` to be shown the full model list (including `latest`).
- Add `--prompt-for-greeting` to paste the greeting text interactively (finish by entering an empty line).

Prompt order is:
1) Voice selection menu
2) Model selection menu
3) Greeting multi-line paste prompt

The greeting text is applied to the first compatible **MessageParticipant** and/or **PlayPrompt** action(s) in the template (if neither exists, the script will fail fast).

```bash
python3 ~/.copilot/skills/connect-elevenlabs-setup/scripts/connect_elevenlabs_setup.py deploy \
  --region us-west-2 \
  --connect-instance-arn arn:aws:connect:us-west-2:ACCOUNT_ID:instance/INSTANCE_ID \
  --template-path "/Users/ChadDHendren/Downloads/1 - Elevenlabs Demo 1.json" \
  --output-path "/Users/ChadDHendren/Downloads/1 - Elevenlabs New Flow.rendered.deployed.json" \
  --secret-name elevenlabs \
  --language en-US \
  --validate-voice \
  --phone-number "+18445935770" \
  --prompt-for-greeting
```

#### Non-interactive deploy (fully specified)

If you pass `--voice-id`, `--model-id`, and `--greeting-text`, the deploy will be fully non-interactive (no menus / no greeting prompt).

#### Flow naming

If you omit `--flow-name`, `deploy` defaults to a unique name like `1 - Elevenlabs <VoiceName> <timestamp>` so the flow name matches the selected voice.
If you provide `--flow-name`, it will create/update that exact name (recommended when you want deterministic naming).

## Connect “Set voice” block rules

- **Model** must be one of the exact ElevenLabs model IDs returned by `/v1/models` (examples: `eleven_multilingual_v2`, `eleven_flash_v2_5`, `eleven_turbo_v2_5`).
- **Do not** prefix with `elevenlabs_`.
- **Voice** should be a `voice_id` (not the friendly voice name).
- If `catalog` shows `category=professional`, ElevenLabs may reject synthesis unless your subscription tier allows Professional voices.
- **Secrets Manager ARN** must point to the secret containing JSON keys `apiToken` and `apiTokenRegion`.

## References

- AWS: Configure third-party TTS providers
  https://docs.aws.amazon.com/connect/latest/adminguide/configure-third-party-tts.html

- AWS: Managing secrets and resource policies (example secret/KMS policies)
  https://docs.aws.amazon.com/connect/latest/adminguide/managing-secrets-resource-policies.html

- Community walkthrough (shows `apiToken`/`apiTokenRegion` schema)
  https://github.com/ensamblador/elevenlabs-voices-amazon-connect
