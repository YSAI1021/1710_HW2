# 3_multi_voices_demo.py
from itertools import product
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEXT = """In 1760, the First Industrial Revolution began mechanizing production with water and steam power.
By the late 1800s, electricity powered mass production at unprecedented scale.
In the 20th century, electronics and computing ushered in automation.
Today, AI and robotics reshape work once again—and we adapt, just as before."""
OUT_DIR = Path("voices_out")
OUT_DIR.mkdir(exist_ok=True)

voices = ["alloy", "verse", "coral"]  # pick 2–5 voices you like
effects = {
    "calm":      "Speak in a calm, neutral tone at a steady pace.",
    "fast":      "Speak 20% faster with energetic emphasis.",
    "narration": "Documentary narrator style, warm and authoritative.",
    "whisper":   "Soft, intimate tone with gentle pauses."
}

for voice, (label, style) in product(voices, effects.items()):
    out_file = OUT_DIR / f"{label}_{voice}.mp3"
    print(f"Generating {out_file.name} ...")
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=TEXT,
        instructions=style  # style/effect hint
    ) as resp:
        resp.stream_to_file(out_file)

print(f"Done. Files in: {OUT_DIR.resolve()}")