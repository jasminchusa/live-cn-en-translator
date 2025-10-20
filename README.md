# CN→EN Realtime Interpreter for Live Streaming (macOS-ready)

A minimal pipeline to interpret Mandarin to English in realtime and feed English audio into OBS for TikTok/YouTube/Twitch.

## Features
- Chunked mic capture + VAD segmentation (low latency)
- `faster-whisper` ASR (good Mandarin accuracy on CPU)
- Translation via OpenAI (gpt-4o-mini), easy to swap provider
- TTS via `edge-tts` (natural voices)
- Plays English into a **virtual audio device** that OBS treats as your mic

## Quick Start (macOS)
1. Install Python 3.10+
2. Install **BlackHole 2ch** (virtual audio device). In Audio MIDI Setup you can create an Aggregate device if needed.
3. In Terminal:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -U pip
   pip install -r requirements.txt
   cp .env.example .env
   # edit .env → set OPENAI_API_KEY and OUTPUT_DEVICE_NAME to 'BlackHole 2ch' if not already
   python app.py
   ```
4. In OBS:
   - Add **Audio Input Capture** = your **BlackHole 2ch** device (this is the English track to stream)
   - Keep your real mic for local monitoring only (mute in program)

## Tips
- If latency is high: set `ASR_MODEL=tiny` in `.env`, reduce `CHUNK_MS` slightly, speak in shorter phrases.
- If OpenAI not available: set `TRANSLATOR_PROVIDER=none` to echo the Chinese as English TTS (for pipeline test).

## Files
- `app.py` main loop
- `audio_io.py` mic/speaker IO
- `asr_whisper.py` whisper wrapper + VAD segmentation
- `translator.py` OpenAI or fallback
- `tts_edge.py` Edge TTS wrapper
- `requirements.txt`, `.env.example`, `utils.py`
