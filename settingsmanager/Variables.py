import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mydb')
your_gpt_api_key = os.getenv('GPT_API_KEY', 'your_gpt_api_key')
ollama_api_url = os.getenv('OLLAMA_API_URL', 'http://localhost:8000/generate')
your_openai_api_key = os.getenv('GPT_API_URL', 'your_openai_api_key')

ollama_api_url =  os.getenv('OLLAMA_API_URL', 'ollama_api_url')

use_gpt = True  # Set to False if using Ollama
use_ollama = not use_gpt