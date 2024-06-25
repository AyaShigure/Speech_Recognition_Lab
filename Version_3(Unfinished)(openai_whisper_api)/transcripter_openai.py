from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key = api_key,
)

audio_file= open("./test.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)