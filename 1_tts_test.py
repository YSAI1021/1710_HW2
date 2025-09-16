from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

# load the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

out_path = Path("python_hello.mp3")

# request TTS and write to file
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="Hello from my Python TTS test!"
) as response:
    response.stream_to_file(out_path)

print("Wrote", out_path.resolve())
