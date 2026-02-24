import os

ollama_BASE_URL = "https://ollama.com/v1"
ollama_model = "qwen3-coder-next"

class Config():
    # providers in order of preference
    if os.getenv("OLLAMA_API_KEY"):
        API_KEY = os.getenv("OLLAMA_API_KEY")
        BASE_URL = ollama_BASE_URL
        MODEL = ollama_model
    elif os.getenv("GROQ_API_KEY"):
        API_KEY = os.getenv("GROQ_API_KEY")
        BASE_URL = "https://api.groq.com/openai/v1"
        MODEL = "openai/gpt-oss-120b"
    else:
        raise RuntimeError("No API key found. Set OPENAI_API_KEY, GROQ_API_KEY, etc.")

config = Config()