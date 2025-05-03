# FitnessLogger

A simple command-line fitness tracking tool for logging workouts, tracking weight, and analyzing progress.

## Features

- Log workout sessions with type, duration, and calories
- Track weight measurements over time
- View fitness statistics and trends
- Workout consistency scoring
- Performance insights and recommendations
- JSON data storage with backup functionality

## Installation

```bash
pip install -e .
```

## Usage

### Log a workout
```bash
python -m src.main workout --type "Running" --duration 30 --calories 250
```

### Record weight
```bash
python -m src.main weight 70.5 --unit kg
```

### View statistics
```bash
# Weekly stats
python -m src.main stats --period week

# Monthly stats with insights
python -m src.main stats --period month
```

## Data Storage

All data is stored locally in JSON format in the `data/` directory. The tool automatically creates backups and handles data persistence.

## Development

Run tests:
```bash
python -m unittest discover tests
```

## Project Structure

```
src/
├── main.py         # CLI interface
├── models.py       # Data models
├── storage.py      # Data persistence
└── analytics.py    # Statistics and insights

tests/
└── test_models.py  # Unit tests
```