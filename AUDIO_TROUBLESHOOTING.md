# Audio Connection Troubleshooting Guide

## Problem: "I can hear the agent speak, but my audio is not being sent"

This guide helps diagnose and fix why the widget isn't capturing your microphone input.

---

## Quick Diagnosis

Use the new **audio diagnostics page** to test your setup:

```bash
# Open this file in your browser:
examples/test_audio_connection.html
```

This will check:
- ✓ Secure connection (HTTPS or localhost)
- ✓ WebRTC support
- ✓ Microphone permissions
- ✓ Agent ID configuration

---

## Common Causes & Fixes

### 1. **Microphone Permission Not Granted**

**Symptom:** Browser never asks for microphone access, or permission was denied.

**Fix:**
1. Open your browser settings
2. Find "Permissions" or "Privacy" → "Microphone"
3. Locate the elevenlabs.io domain
4. Set to "Allow"
5. Refresh the page and retry

**Chrome:**
- Click the lock icon in address bar → Permissions → Microphone → Allow

**Firefox:**
- Firefox menu → Settings → Privacy → Permissions → Microphone → Allow for elevenlabs.io

**Safari:**
- Safari → Preferences → Websites → Microphone → Allow

---

### 2. **Agent ID Not Configured**

**Symptom:** Widget appears but doesn't connect.

**Check:**
- Open browser DevTools (F12)
- In Console tab, look for errors mentioning "agent-id" or "AGENT_ID_HERE"

**Fix:**
1. Get your agent ID from ElevenLabs dashboard:
   - https://elevenlabs.io/app/conversational-ai
2. Copy your agent ID
3. In `widget_demo.html`, replace `AGENT_ID_HERE` with your actual ID:
   ```html
   <elevenlabs-convai agent-id="YOUR_AGENT_ID_HERE"></elevenlabs-convai>
   ```
4. Save and reload the page

---

### 3. **Not Using HTTPS (or not localhost)**

**Symptom:** Browser won't allow microphone access; security warning in console.

**Why:** Modern browsers require HTTPS for microphone access (except localhost).

**Fix Options:**

**Option A: Use localhost (Recommended for testing)**
```bash
# Python 3
cd elevenlabs-connect
python -m http.server 8000

# Then open: http://localhost:8000/examples/widget_demo.html
```

**Option B: Deploy to HTTPS**
- Use GitHub Pages, Vercel, or Netlify (all free)
- These automatically provide HTTPS

**Option C: Use ngrok tunnel**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000

# Use the HTTPS URL it provides
```

---

### 4. **WebRTC Not Supported**

**Symptom:** Diagnostics show "WebRTC not available"

**This is rare**, but can happen with:
- Very old browsers (IE, ancient Safari)
- Older versions of mobile browsers

**Fix:** Update browser to latest version

---

### 5. **No Microphone Hardware**

**Symptom:** Browser gives "No microphone found" error

**Check:**
- System audio settings → Microphone enabled?
- Is mic plugged in (if external)?
- Test mic in system settings first

**Fix:** Enable or connect microphone hardware

---

### 6. **Browser Extension Blocking Audio**

**Symptom:** Microphone permission shows "Allow" but still doesn't work

**Common culprits:**
- Privacy extensions (uBlock Origin, Privacy Badger, etc.)
- VPN extensions
- Ad blockers

**Fix:**
1. Disable extensions temporarily
2. Test the widget
3. If it works, re-enable extensions one by one to find the culprit
4. Add elevenlabs.io to extension whitelist

---

## Debug Mode

Enable detailed logging in browser console:

1. Open DevTools (F12)
2. Paste this in Console:
   ```javascript
   // Log all widget events
   document.addEventListener('elevenlabs:user-message', (e) => {
       console.log('👤 User message:', e.detail);
   });
   
   document.addEventListener('elevenlabs:agent-message', (e) => {
       console.log('🤖 Agent message:', e.detail);
   });
   
   document.addEventListener('elevenlabs:conversation-started', () => {
       console.log('✓ Conversation started - check microphone now');
   });
   ```

3. Start a conversation and check console output
4. If you see user messages logged, audio is being captured
5. If you see agent messages but no user messages, microphone isn't being captured

---

## Testing Checklist

- [ ] Using HTTPS or localhost? (run diagnostics to check)
- [ ] Microphone permission granted? (check in browser settings)
- [ ] Agent ID configured? (replaced AGENT_ID_HERE with real ID)
- [ ] Microphone working in system settings?
- [ ] No browser extensions blocking audio?
- [ ] Running latest browser version?

---

## If Still Not Working

Check the browser console (F12) for error messages. Look for:

**Error: "agent-id missing"**
→ Replace AGENT_ID_HERE in HTML

**Error: "getUserMedia permission denied"**
→ Grant microphone permission in browser settings

**Error: "WebSocket connection failed"**
→ Check Agent ID is valid in ElevenLabs dashboard

**Error: "Not secure"**
→ Use HTTPS or localhost

---

## Test the Backend

If the widget still won't work, test that your agent exists and is functional:

```bash
# From elevenlabs-connect directory
python examples/quickstart.py
```

This will list your agents and show if they're responding.

---

## Contact ElevenLabs Support

If issues persist:
- https://elevenlabs.io/docs
- https://elevenlabs.io/support
- Provide your agent ID and browser console errors
