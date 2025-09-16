# 2_streaming_tts_test.py
import asyncio, os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import sounddevice as sd
import numpy as np

# ---- config ----
OUTPUT_DEVICE_INDEX = None  # set to an integer from list_devices.py, e.g., 0 or 1; leave None to use default
VOICE = "alloy"
TEXT_FILE = Path("narration.txt")
# ----------------

def beep(ms=400, freq=660, volume=0.2, sr=44100):
    t = np.linspace(0, ms/1000, int(sr*ms/1000), False)
    sd.play(volume*np.sin(2*np.pi*freq*t), sr)
    sd.wait()

async def main():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not found; check your .env and load_dotenv()")

    if not TEXT_FILE.exists():
        TEXT_FILE.write_text("Streaming test. You should hear this immediately as it is generated.", encoding="utf-8")

    # Optional: select output device explicitly
    if OUTPUT_DEVICE_INDEX is not None:
        sd.default.device = (sd.default.device[0], OUTPUT_DEVICE_INDEX)

    # Quick audible check
    beep()
    print("✔ Beep played on current output device.")

    client = AsyncOpenAI()
    player = LocalAudioPlayer()  # uses sounddevice under the hood

    text = TEXT_FILE.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("narration.txt is empty")

    print("Requesting streaming TTS… (you should hear audio start in ~1–2s if quota is available)")
    try:
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=VOICE,
            input=text,
        ) as response:
            await player.play(response)
        print("✔ Streaming finished.")
    except Exception as e:
        print("✖ Streaming error:", e)
        print("Tip: If you recently saw 429/insufficient_quota, add billing or raise your monthly cap, then retry.")

if __name__ == "__main__":
    asyncio.run(main())
