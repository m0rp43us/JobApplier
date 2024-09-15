import requests
import json
import config

class OllamaWrapper(AIModel):
    def __init__(self):
        self.api_url = config.ollama_api_url

    def generate_response(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"prompt": prompt})
        response = requests.post(self.api_url, headers=headers, data=data)
        response_data = response.json()
        return response_data.get('response', '')
