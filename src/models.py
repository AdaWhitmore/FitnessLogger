from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, List
import json

@dataclass
class WorkoutEntry:
    date: datetime
    exercise_type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    notes: str = ""

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'exercise_type': self.exercise_type,
            'duration_minutes': self.duration_minutes,
            'calories_burned': self.calories_burned,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date=datetime.fromisoformat(data['date']),
            exercise_type=data['exercise_type'],
            duration_minutes=data['duration_minutes'],
            calories_burned=data.get('calories_burned'),
            notes=data.get('notes', '')
        )

@dataclass
class WeightEntry:
    date: datetime
    weight: float
    unit: str = "kg"

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'weight': self.weight,
            'unit': self.unit
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date=datetime.fromisoformat(data['date']),
            weight=data['weight'],
            unit=data.get('unit', 'kg')
        )

@dataclass
class FitnessProfile:
    workouts: List[WorkoutEntry] = field(default_factory=list)
    weight_history: List[WeightEntry] = field(default_factory=list)

    def add_workout(self, workout: WorkoutEntry):
        self.workouts.append(workout)

    def add_weight_entry(self, weight_entry: WeightEntry):
        self.weight_history.append(weight_entry)

    def get_recent_workouts(self, days: int = 7) -> List[WorkoutEntry]:
        cutoff = datetime.now() - timedelta(days=days)
        return [w for w in self.workouts if w.date >= cutoff]

    def to_dict(self):
        return {
            'workouts': [w.to_dict() for w in self.workouts],
            'weight_history': [w.to_dict() for w in self.weight_history]
        }

    @classmethod
    def from_dict(cls, data):
        profile = cls()
        profile.workouts = [WorkoutEntry.from_dict(w) for w in data.get('workouts', [])]
        profile.weight_history = [WeightEntry.from_dict(w) for w in data.get('weight_history', [])]
        return profile