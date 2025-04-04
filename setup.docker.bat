@echo off
docker pull ollama/ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull qwen2.5
curl http://localhost:11434/api/tags
