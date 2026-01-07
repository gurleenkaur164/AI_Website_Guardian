#LLM Brain
import requests
import os

OLLAMA_MODEL= os.getenv("OLLAMA_MODEL",  "llama3")
OLLAMA_URL= "http://localhost:11434/api/generate"

def ask_llm(prompt:str)-> str:
    payload={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream":False
    }

    response= requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"].strip()