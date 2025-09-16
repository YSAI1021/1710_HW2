source .env
curl https://api.openai.com/v1/audio/speech -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" -d '{"model":"gpt-4o-mini-tts","voice":"alloy","input":"Hello from my first OpenAI TTS test!"}' --output hello.mp3

