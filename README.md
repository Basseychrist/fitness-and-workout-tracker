# Fitness & Workout Tracker (Terminal)

A terminal-based fitness tracker that stores workouts and user profiles in Google Firestore.

Requirements
- Python 3.8+
- A Firebase service account JSON (see `firebase_key.json`) and project with Firestore enabled.

Setup
1. Place your service account `firebase_key.json` in the project root or set environment variable `FIREBASE_KEY_PATH` to its path.
2. (Optional) create a virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Running
- Start interactive CLI:

```bash
python tracker.py
```

- Run the demo (creates a profile and a workout):

```bash
python sample_demo.py
```

Data model
- `user_profiles` collection: stores basic user info.
- `workouts` collection: each document contains `profile_ref` (a reference to a `user_profiles` document) and workout fields such as `date`, `workout_type`, `duration_minutes`, and `calories_burned`.

Notes
- `firebase_key.json` is added to `.gitignore` to avoid committing secrets.
