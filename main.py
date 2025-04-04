from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import ollama
import asyncio
from edge_tts import Communicate
import os

ollama.base_url = "http://localhost:11434"
model = "qwen2.5"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_ollama(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        content = response['message']['content']
        asyncio.create_task(speak(content))
        return JSONResponse({"response": content})
    except Exception as e:
        return JSONResponse({"error": str(e)})

async def speak(text):
    communicate = Communicate(text, "en-US-AriaNeural")
    await communicate.save("audio\response.mp3")
    os.system("start audio\response.mp3")
