# Live in a Trailer

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

Narrate your life like a movie trailer. Send the app an image and it describes the scene in 1–3 short, dramatic cliffhanger sentences — then voices it in a deep, booming movie-trailer voice.

## How it works

- A web page sends a captured image to the `/analyze` endpoint
- GPT-4o describes it in the style of a movie-trailer voice-over (everything is a cliffhanger)
- ElevenLabs converts the line into a dramatic trailer voice and returns the audio

## Setup

Requires `OPENAI_API_KEY` and `ELEVENLABS_API_KEY` in a `.env` file.

```bash
pip install flask python-dotenv requests openai pygame
python screenshot_analyzer.py
```

Opens a Flask dev server; visit the served page in your browser.

## Tech

Flask, OpenAI (GPT-4o vision), ElevenLabs TTS.
