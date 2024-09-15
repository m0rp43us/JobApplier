from pymongo import MongoClient
from jobapplier.aihelper.GptWrapper import GptWrapper
from jobapplier.aihelper.OllamaWrapper import OllamaWrapper
from settingsmanager.SettingsManager import SettingsManager
import config

class QuestionManager:
    def __init__(self):
        self.db = self._get_database()
        self.settings = SettingsManager.getsettings()
        self.ai_model = self._initialize_model()
        self.cached_strategy = CachedResponseStrategy(self.db)
        self.direct_strategy = DirectAIQueryStrategy(self.ai_model)

    def _get_database(self):
        """Initialize MongoDB client and get the database."""
        client = MongoClient(config.MONGO_URI)
        return client.get_database()

    def _initialize_model(self):
        """Initialize the AI model based on settings."""
        if self.settings.use_gpt:
            return GptWrapper()
        elif self.settings.use_ollama:
            return OllamaWrapper()
        else:
            raise ValueError("No AI model configuration provided.")

    def get_response(self, question: str) -> str:
        """Get response to a question, using cache or AI model as needed."""
        # First, try to get a cached response
        cached_response = self.cached_strategy.get_response(question)
        
        if cached_response:
            # If a cached response is found, refine it with the AI model
            refined_prompt = self._create_refined_prompt(question, cached_response)
            response = self.direct_strategy.get_response(refined_prompt)
        else:
            # If no cached response, get a direct response from the AI model
            response = self.direct_strategy.get_response(question)
            # Save the new response to the database
            self._save_to_database(question, response)

        return response

    def _create_refined_prompt(self, question: str, cached_response: str) -> str:
        """Create a prompt that incorporates cached data."""
        return f"Based on the following information, provide a detailed response. Information: {cached_response}. Question: {question}"

    def _save_to_database(self, question: str, response: str):
        """Save the question and response to MongoDB."""
        collection = self.db.questions
        collection.insert_one({"question": question, "response": response})

class DirectAIQueryStrategy:
    def __init__(self, ai_model):
        self.ai_model = ai_model

    def get_response(self, prompt: str) -> str:
        """Directly query the AI model for the response."""
        return self.ai_model.generate_response(prompt)

class CachedResponseStrategy:
    def __init__(self, db):
        self.db = db

    def get_response(self, question: str) -> str:
        """Check the database for a cached response."""
        response = self._query_database(question)
        return response

    def _query_database(self, question: str) -> str:
        """Query the MongoDB database for the question."""
        collection = self.db.questions
        doc = collection.find_one({"question": question})
        if doc:
            return doc.get("response")
        return None
