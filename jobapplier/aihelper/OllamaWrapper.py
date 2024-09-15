import requests
import json
import config


class OllamaWrapper:
    def __init__(self):
        setings = SettingsManager.getsettings()
        openai.api_key = setings.openai_api_key

    def get_response(self, prompt):
        response = requests.post(
            self.api_url,
            json={"prompt": prompt}
        )
        response_json = response.json()
        return response_json.get("response", "")

