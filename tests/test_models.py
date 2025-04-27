import unittest
from datetime import datetime
from src.models import WorkoutEntry, WeightEntry, FitnessProfile

class TestModels(unittest.TestCase):

    def test_workout_entry_creation(self):
        workout = WorkoutEntry(
            date=datetime.now(),
            exercise_type="Running",
            duration_minutes=30,
            calories_burned=300
        )
        self.assertEqual(workout.exercise_type, "Running")
        self.assertEqual(workout.duration_minutes, 30)

    def test_workout_serialization(self):
        workout = WorkoutEntry(
            date=datetime(2023, 4, 15, 10, 30),
            exercise_type="Cycling",
            duration_minutes=45
        )

        data = workout.to_dict()
        restored = WorkoutEntry.from_dict(data)

        self.assertEqual(workout.exercise_type, restored.exercise_type)
        self.assertEqual(workout.duration_minutes, restored.duration_minutes)
        self.assertEqual(workout.date, restored.date)

    def test_weight_entry(self):
        weight = WeightEntry(
            date=datetime.now(),
            weight=70.5,
            unit="kg"
        )
        self.assertEqual(weight.weight, 70.5)
        self.assertEqual(weight.unit, "kg")

    def test_fitness_profile(self):
        profile = FitnessProfile()

        workout = WorkoutEntry(
            date=datetime.now(),
            exercise_type="Swimming",
            duration_minutes=60
        )

        profile.add_workout(workout)
        self.assertEqual(len(profile.workouts), 1)

if __name__ == '__main__':
    unittest.main()