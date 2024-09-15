import openai
from jobapplier.aihelper.AiHelper import AIModel
from settingsmanager.SettingsManager import SettingsManager

class GptWrapper(AIModel):
    def __init__(self):
        setings = SettingsManager.getsettings()
        openai.api_key = setings.openai_api_key

    def get_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another engine if needed
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
