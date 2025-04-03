@echo off
python -m venv ollama_env
ollama_env\Scripts\activate
pip install --upgrade pip
pip install speechrecognition ollama pyttsx3 edge-tts
