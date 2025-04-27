from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import math

from .models import WorkoutEntry, WeightEntry, FitnessProfile

class FitnessAnalytics:
    def __init__(self, profile: FitnessProfile):
        self.profile = profile

    def get_workout_frequency(self, days: int = 30) -> Dict[str, int]:
        cutoff = datetime.now() - timedelta(days=days)
        recent_workouts = [w for w in self.profile.workouts if w.date >= cutoff]

        workout_types = Counter(w.exercise_type for w in recent_workouts)
        return dict(workout_types)

    def get_weekly_summary(self, weeks_back: int = 4) -> List[Dict]:
        summaries = []

        for week in range(weeks_back):
            start_date = datetime.now() - timedelta(weeks=week+1)
            end_date = datetime.now() - timedelta(weeks=week)

            week_workouts = [
                w for w in self.profile.workouts
                if start_date <= w.date < end_date
            ]

            total_duration = sum(w.duration_minutes for w in week_workouts)
            total_calories = sum(w.calories_burned for w in week_workouts if w.calories_burned)

            summaries.append({
                'week_start': start_date.strftime('%Y-%m-%d'),
                'workouts_count': len(week_workouts),
                'total_duration': total_duration,
                'total_calories': total_calories,
                'avg_duration': total_duration / len(week_workouts) if week_workouts else 0
            })

        return summaries

    def weight_trend(self, days: int = 90) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        recent_weights = [w for w in self.profile.weight_history if w.date >= cutoff]

        if len(recent_weights) < 2:
            return {'trend': 'insufficient_data', 'change': 0}

        recent_weights.sort(key=lambda x: x.date)
        first_weight = recent_weights[0].weight
        last_weight = recent_weights[-1].weight

        change = last_weight - first_weight
        trend = 'stable'

        if abs(change) > 0.5:  # significant change threshold
            trend = 'increasing' if change > 0 else 'decreasing'

        return {
            'trend': trend,
            'change': round(change, 1),
            'period_days': (recent_weights[-1].date - recent_weights[0].date).days,
            'data_points': len(recent_weights)
        }

    def workout_consistency_score(self, days: int = 30) -> float:
        cutoff = datetime.now() - timedelta(days=days)
        recent_workouts = [w for w in self.profile.workouts if w.date >= cutoff]

        if not recent_workouts:
            return 0.0

        # Calculate days with workouts
        workout_dates = set(w.date.date() for w in recent_workouts)
        total_days = days
        workout_days = len(workout_dates)

        # Basic consistency score
        consistency = workout_days / total_days

        # Bonus for even distribution (reduce clustering penalty)
        if workout_days > 1:
            recent_workouts.sort(key=lambda x: x.date)
            gaps = []
            for i in range(1, len(workout_dates)):
                gap = (sorted(workout_dates)[i] - sorted(workout_dates)[i-1]).days
                gaps.append(gap)

            avg_gap = sum(gaps) / len(gaps)
            ideal_gap = total_days / workout_days

            # Reduce score if gaps are very uneven
            gap_variance = sum((gap - avg_gap) ** 2 for gap in gaps) / len(gaps)
            consistency *= max(0.5, 1 - (gap_variance / (ideal_gap ** 2)))

        return min(1.0, consistency)

    def performance_insights(self) -> List[str]:
        insights = []

        # Recent activity
        recent_workouts = self.profile.get_recent_workouts(7)
        if len(recent_workouts) == 0:
            insights.append("No workouts logged in the past week")
        elif len(recent_workouts) >= 3:
            insights.append("Great activity level this week!")

        # Weight trend
        weight_data = self.weight_trend(30)
        if weight_data['trend'] == 'decreasing':
            insights.append(f"Weight trending down by {abs(weight_data['change'])} kg over {weight_data['period_days']} days")
        elif weight_data['trend'] == 'increasing':
            insights.append(f"Weight trending up by {weight_data['change']} kg")

        # Consistency
        consistency = self.workout_consistency_score(30)
        if consistency >= 0.7:
            insights.append("Excellent workout consistency!")
        elif consistency >= 0.4:
            insights.append("Good workout routine, try to be more consistent")
        else:
            insights.append("Try to workout more regularly for better results")

        # Most frequent exercise
        frequency = self.get_workout_frequency(30)
        if frequency:
            top_exercise = max(frequency.items(), key=lambda x: x[1])
            insights.append(f"Most frequent exercise: {top_exercise[0]} ({top_exercise[1]} times)")

        return insights