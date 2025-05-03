from datetime import datetime
import os

def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes == 0:
        return f"{hours}h"
    return f"{hours}h {remaining_minutes}m"

def get_data_dir() -> str:
    data_dir = os.path.expanduser("~/.fitness_logger")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def parse_workout_type(exercise_type: str) -> str:
    # Normalize workout type names
    type_mapping = {
        'run': 'Running',
        'running': 'Running',
        'bike': 'Cycling',
        'cycling': 'Cycling',
        'swim': 'Swimming',
        'swimming': 'Swimming',
        'gym': 'Strength Training',
        'weights': 'Strength Training',
        'yoga': 'Yoga',
        'walk': 'Walking',
        'walking': 'Walking'
    }

    return type_mapping.get(exercise_type.lower(), exercise_type.title())

def validate_positive_number(value: float, name: str) -> bool:
    if value <= 0:
        print(f"Error: {name} must be a positive number")
        return False
    return True