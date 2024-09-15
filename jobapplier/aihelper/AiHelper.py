from jobapplier.aihelper.GptWrapper import GptWrapper
from jobapplier.aihelper.OllamaWrapper import OllamaWrapper
from settingsmanager.SettingsManager import SettingsManager
from abc import ABC, abstractmethod

class AIModel(ABC):
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        pass


class AIHelper:
    def __init__(self):
        self.settings = SettingsManager.getsettings()
        self.model = self._initialize_model()

    def _initialize_model(self):
        if self.settings.use_gpt:
            return AIModel(GptWrapper())
        elif self.settings.use_ollama:
            return AIModel(OllamaWrapper())
        else:
            raise ValueError("No AI model configuration provided.")

    def get_response(self, prompt: str) -> str:
        return self.model.generate_response(prompt)
