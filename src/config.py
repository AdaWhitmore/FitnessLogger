import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "data_directory": "data",
    "default_weight_unit": "kg",
    "backup_frequency": "weekly",
    "max_backups": 5,
    "date_format": "%Y-%m-%d",
    "workout_types": [
        "Running",
        "Cycling",
        "Swimming",
        "Strength Training",
        "Yoga",
        "Walking",
        "Cardio",
        "Stretching"
    ]
}

class Config:
    def __init__(self):
        self.config_file = Path("config.json")
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = DEFAULT_CONFIG.copy()
                    config.update(user_config)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")

        return DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()