import requests
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_URL = "http://localhost:11434/api/chat"

def chat(messages, tools=None):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    if tools:
        payload["tools"] = tools

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["message"]
