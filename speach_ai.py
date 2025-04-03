import speech_recognition as sr
import ollama
import pyttsx3
import asyncio
from edge_tts import Communicate
import os

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set Ollama to use Qwen2.5 running in Docker
ollama.base_url = "http://localhost:11434"

def recognize_speech():
    """Captures speech and converts it to text"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results.")
            return None

def query_ollama(prompt):
    """Sends text to Qwen2.5 in Ollama Docker and returns the response"""
    response = ollama.chat(model="qwen2.5", messages=[{"role": "user", "content": prompt}])
    ai_response = response['message']['content']
    print(f"Qwen2.5 says: {ai_response}")
    return ai_response

async def speak_text(text):
    """Uses Edge-TTS for realistic speech output"""
    communicate = Communicate(text, "en-US-AriaNeural")
    await communicate.save("response.mp3")
    os.system("mpg123 response.mp3")  # Use VLC or another player if mpg123 is unavailable

def main():
    while True:
        text = recognize_speech()
        if text:
            ai_response = query_ollama(text)
            asyncio.run(speak_text(ai_response))

if __name__ == "__main__":
    main()
