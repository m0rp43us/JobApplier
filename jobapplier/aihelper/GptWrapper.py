import openai
import SetingsManager
from jobapplier.aihelper.AIModel import AIModel

class GptWrapper(AIModel):
    def __init__(self):
        setings = SetingsManager.getsettings()
        openai.api_key = setings.openai_api_key

    def generate_response(self, prompt: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use your preferred engine
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
