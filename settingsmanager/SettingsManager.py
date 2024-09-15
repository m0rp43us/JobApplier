import os
from singleton_decorator import singleton

@singleton
class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        settings = {
            "api_key": os.getenv("API_KEY", ""),
            "database_url": os.getenv("DATABASE_URL", ""),
            "timeout": int(os.getenv("TIMEOUT", "60")),
            # Add other settings as needed
        }
        return settings

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        # Optionally, update environment variables or persist settings elsewhere

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.settings[key] = value
        # Optionally, update environment variables or persist settings elsewhere

    def remove(self, key):
        if key in self.settings:
            del self.settings[key]
            # Optionally, remove from environment variables or persist changes elsewhere

    def reload(self):
        self.settings = self.load_settings()

# Example usage
if __name__ == "__main__":
    # Retrieve settings
    manager = SettingsManager()
    print(manager.get('api_key'))

    # Set new value
    manager.set('api_key', 'new_api_key')

    # Update multiple settings
    manager.update(api_key='another_api_key', timeout=30)

    # Remove a setting
    manager.remove('old_setting')

    # Reload settings from environment variables
    manager.reload()
