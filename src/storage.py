import json
import os
from pathlib import Path
from typing import Optional
from .models import FitnessProfile

class DataStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.profile_file = self.data_dir / "fitness_profile.json"

    def save_profile(self, profile: FitnessProfile) -> bool:
        try:
            with open(self.profile_file, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False

    def load_profile(self) -> Optional[FitnessProfile]:
        if not self.profile_file.exists():
            return FitnessProfile()

        try:
            with open(self.profile_file, 'r') as f:
                data = json.load(f)
            return FitnessProfile.from_dict(data)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return FitnessProfile()

    def backup_data(self, backup_name: str = None) -> bool:
        if not self.profile_file.exists():
            return False

        if backup_name is None:
            from datetime import datetime
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_file = self.data_dir / f"{backup_name}.json"

        try:
            import shutil
            shutil.copy2(self.profile_file, backup_file)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def list_backups(self) -> list:
        backup_files = list(self.data_dir.glob("backup_*.json"))
        return [f.name for f in backup_files]