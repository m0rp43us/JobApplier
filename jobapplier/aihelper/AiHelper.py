import config

class AIHelper:
    def __init__(self):
        self.model = self._initialize_model()

    def _initialize_model(self):
        if config.use_gpt:
            return GptWrapper()
        elif config.use_ollama:
            return OllamaWrapper()
        else:
            raise ValueError("No AI model configuration provided.")

    def get_response(self, prompt: str) -> str:
        return self.model.generate_response(prompt)