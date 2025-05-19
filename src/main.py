#!/usr/bin/env python3
"""
FitnessLogger - Personal Fitness Tracking Tool
A simple command-line tool to track workouts, nutrition, and progress.
"""

import argparse
import sys
import json
from datetime import datetime
from .models import WorkoutEntry, WeightEntry
from .storage import DataStorage
from .utils import parse_workout_type, validate_positive_number

def handle_workout(args):
    if args.duration and not validate_positive_number(args.duration, "duration"):
        return
    if args.calories and not validate_positive_number(args.calories, "calories"):
        return

    storage = DataStorage()
    profile = storage.load_profile()

    exercise_type = parse_workout_type(args.type)

    workout = WorkoutEntry(
        date=datetime.now(),
        exercise_type=exercise_type,
        duration_minutes=args.duration or 0,
        calories_burned=args.calories,
        notes=args.notes or ""
    )

    profile.add_workout(workout)

    if storage.save_profile(profile):
        print(f"Workout logged: {exercise_type} for {workout.duration_minutes} minutes")
        if workout.calories_burned:
            print(f"Calories burned: {workout.calories_burned}")
    else:
        print("Error saving workout data")

def handle_weight(args):
    if not validate_positive_number(args.value, "weight"):
        return

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

        # Show change from last entry if available
        if len(profile.weight_history) > 1:
            prev_weight = profile.weight_history[-2].weight
            change = args.value - prev_weight
            direction = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"Change: {direction} {abs(change):.1f} {args.unit}")
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

def handle_list(args):
    storage = DataStorage()
    profile = storage.load_profile()

    recent_workouts = profile.get_recent_workouts(args.days)

    if not recent_workouts:
        print(f"No workouts found in the last {args.days} days")
        return

    print(f"=== Recent Workouts (last {args.days} days) ===")

    recent_workouts.sort(key=lambda x: x.date, reverse=True)

    for workout in recent_workouts:
        date_str = workout.date.strftime("%Y-%m-%d %H:%M")
        duration = f"{workout.duration_minutes}min" if workout.duration_minutes else "N/A"
        calories = f", {workout.calories_burned} cal" if workout.calories_burned else ""

        print(f"{date_str} - {workout.exercise_type} ({duration}{calories})")
        if workout.notes:
            print(f"  Notes: {workout.notes}")

def handle_export(args):
    storage = DataStorage()
    profile = storage.load_profile()

    if args.format == 'json':
        data = profile.to_dict()
        output = json.dumps(data, indent=2, default=str)
    elif args.format == 'csv':
        import csv
        import io

        output_buffer = io.StringIO()

        # Write workouts
        writer = csv.writer(output_buffer)
        writer.writerow(['Date', 'Type', 'Duration (min)', 'Calories', 'Notes'])

        for workout in profile.workouts:
            writer.writerow([
                workout.date.strftime('%Y-%m-%d %H:%M'),
                workout.exercise_type,
                workout.duration_minutes,
                workout.calories_burned or '',
                workout.notes
            ])

        output = output_buffer.getvalue()

    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Data exported to {args.output}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print(output)

def main():
    parser = argparse.ArgumentParser(description='Personal Fitness Logger')
    parser.add_argument('--version', action='version', version='FitnessLogger 0.2.0')

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

    # List workouts command
    list_parser = subparsers.add_parser('list', help='List recent workouts')
    list_parser.add_argument('--days', type=int, default=7, help='Number of days to show')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--format', default='json', choices=['json', 'csv'])
    export_parser.add_argument('--output', help='Output file path')

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
    elif args.command == 'list':
        handle_list(args)
    elif args.command == 'export':
        handle_export(args)

if __name__ == '__main__':
    main()