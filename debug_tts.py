from pathlib import Path
import os, sys, traceback
from dotenv import load_dotenv

print("=== DEBUG START ===")
print("CWD:", Path.cwd())
print("Python:", sys.version)
try:
    import openai
    from openai import OpenAI
    print("openai package version:", openai.__version__)
except Exception as e:
    print("OpenAI SDK not importable:", e)
    print("Try: pip install --upgrade openai \"openai[voice_helpers]\" python-dotenv")
    sys.exit(1)

# 1) Load .env and check key presence (without printing it)
load_dotenv()
has_key = bool(os.getenv("OPENAI_API_KEY"))
print("OPENAI_API_KEY present:", has_key)
if not has_key:
    print("ERROR: OPENAI_API_KEY not found. Ensure .env contains exactly one line:\nOPENAI_API_KEY=sk-...")
    sys.exit(1)

# 2) Attempt a TTS call and write the file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
out_path = Path("python_hello.mp3")

try:
    print("Calling TTS…")
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input="Hello from my Python TTS test!"
    ) as resp:
        resp.stream_to_file(out_path)

    print("Wrote file:", out_path.resolve())
    print("Exists:", out_path.exists(), "Size:", out_path.stat().st_size if out_path.exists() else 0, "bytes")
except Exception as e:
    print("ERROR during TTS call:")
    traceback.print_exc()
    sys.exit(1)

print("=== DEBUG END ===")
