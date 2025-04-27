#!/usr/bin/env python3
"""
FitnessLogger - Personal Fitness Tracking Tool
A simple command-line tool to track workouts, nutrition, and progress.
"""

import argparse
import sys
from datetime import datetime
from .models import WorkoutEntry, WeightEntry
from .storage import DataStorage

def handle_workout(args):
    storage = DataStorage()
    profile = storage.load_profile()

    workout = WorkoutEntry(
        date=datetime.now(),
        exercise_type=args.type,
        duration_minutes=args.duration or 0,
        calories_burned=args.calories,
        notes=args.notes or ""
    )

    profile.add_workout(workout)

    if storage.save_profile(profile):
        print(f"Workout logged: {args.type} for {workout.duration_minutes} minutes")
    else:
        print("Error saving workout data")

def handle_weight(args):
    storage = DataStorage()
    profile = storage.load_profile()

    weight_entry = WeightEntry(
        date=datetime.now(),
        weight=args.value,
        unit=args.unit
    )

    profile.add_weight_entry(weight_entry)

    if storage.save_profile(profile):
        print(f"Weight logged: {args.value} {args.unit}")
    else:
        print("Error saving weight data")

def handle_stats(args):
    from .analytics import FitnessAnalytics

    storage = DataStorage()
    profile = storage.load_profile()
    analytics = FitnessAnalytics(profile)

    print(f"=== Fitness Stats ({args.period}) ===")

    if args.period == 'week':
        recent_workouts = profile.get_recent_workouts(7)
        days = 7
    elif args.period == 'month':
        recent_workouts = profile.get_recent_workouts(30)
        days = 30
    else:
        recent_workouts = profile.workouts
        days = 365

    print(f"Total workouts: {len(recent_workouts)}")

    if recent_workouts:
        total_duration = sum(w.duration_minutes for w in recent_workouts)
        print(f"Total exercise time: {total_duration} minutes")

        total_calories = sum(w.calories_burned for w in recent_workouts if w.calories_burned)
        if total_calories > 0:
            print(f"Total calories burned: {total_calories}")

    # Show analytics insights
    if args.period == 'month':
        consistency = analytics.workout_consistency_score(30)
        print(f"Workout consistency: {consistency:.1%}")

        weight_trend = analytics.weight_trend(30)
        if weight_trend['trend'] != 'insufficient_data':
            print(f"Weight trend: {weight_trend['trend']} ({weight_trend['change']:+.1f} kg)")

    # Show current weight
    if profile.weight_history:
        latest_weight = profile.weight_history[-1]
        print(f"Current weight: {latest_weight.weight} {latest_weight.unit}")

    # Performance insights
    if args.period == 'month':
        print("\n--- Insights ---")
        for insight in analytics.performance_insights():
            print(f"• {insight}")

def main():
    parser = argparse.ArgumentParser(description='Personal Fitness Logger')
    parser.add_argument('--version', action='version', version='FitnessLogger 0.1.0')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Workout commands
    workout_parser = subparsers.add_parser('workout', help='Log workout sessions')
    workout_parser.add_argument('--type', required=True, help='Type of workout')
    workout_parser.add_argument('--duration', type=int, help='Duration in minutes')
    workout_parser.add_argument('--calories', type=int, help='Calories burned')
    workout_parser.add_argument('--notes', help='Additional notes')

    # Weight tracking
    weight_parser = subparsers.add_parser('weight', help='Log weight measurements')
    weight_parser.add_argument('value', type=float, help='Weight value')
    weight_parser.add_argument('--unit', default='kg', choices=['kg', 'lbs'])

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='View fitness statistics')
    stats_parser.add_argument('--period', default='week', choices=['week', 'month', 'year'])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'workout':
        handle_workout(args)
    elif args.command == 'weight':
        handle_weight(args)
    elif args.command == 'stats':
        handle_stats(args)

if __name__ == '__main__':
    main()