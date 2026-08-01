# Overview

This project is a Fitness & Workout Tracker I built to practice building a small full-stack workflow: a local Python app integrated with a cloud NoSQL database for persistent storage. The goals were to implement reliable CRUD operations, learn how to model relations in Firestore using document references, and provide both a terminal and a simple GUI to interact with the data.

The software is a lightweight tracker that lets users create profiles and log workout sessions. It stores user profiles and workouts in Google Firestore and provides the following ways to use it:

- Command-line interactive interface: run `python tracker.py` for a terminal menu.
- Graphical interface (Tkinter): run `python tracker_gui.py` for a simple desktop UI.
- Demo script that exercises basic CRUD: run `python sample_demo.py`.

You will need a Firebase service account JSON file (place it at `firebase_key.json` or set `FIREBASE_KEY_PATH` to the path).

[Software Demo Video](https://youtu.be/iER4Y_1adZI?si=VzoysRC34rNoTzRX)

# Cloud Database

This project uses Google Firestore (part of Firebase / Google Cloud) as the cloud NoSQL database. Firestore is a document store that organizes data into collections and documents.

Database structure created for this project:

- Collection `user_profiles`: each document holds a user profile with fields like `name`, `age`, `weight_kg`, `goals`, and `created_at`.
- Collection `workouts`: each document holds a workout record with fields `date`, `workout_type`, `duration_minutes`, `calories_burned`, `created_at`, and `profile_ref`.

`profile_ref` is a Firestore `DocumentReference` that points to a document in `user_profiles`, providing a relation between a workout and its owner.

# Development Environment

- Language: Python 3.8+
- Main libraries:
	- `firebase-admin` (Admin SDK) — authenticates using a service account and connects to Firestore
	- `google-cloud-firestore` — low-level Firestore client used by the admin SDK
	- `tkinter` — standard Python GUI library (bundled with Python on most platforms)

- Tools used:
	- Git for version control
	- VS Code for editing and running scripts

Setup and run (example):

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
set FIREBASE_KEY_PATH=path\to\your\firebase_key.json   # Windows example
python tracker.py         # terminal UI
python tracker_gui.py     # graphical UI
python sample_demo.py     # demo script
```

# Useful Websites

- [Firebase Admin Python SDK docs](https://firebase.google.com/docs/admin/setup)
- [Cloud Firestore documentation](https://firebase.google.com/docs/firestore)
- [google-cloud-firestore Python client](https://googleapis.dev/python/firestore/latest/index.html)
- [Tkinter reference (TkDocs)](https://tkdocs.com/)

# Future Work

- Add user authentication and scoped access so users can only modify their own data.
- Add pagination and date-range filters for listing large numbers of workouts.
- Improve the GUI (search, sorting, inline edit) and add unit tests for key functions.
- Add exporting (CSV) and simple analytics (weekly totals, calories burned trends)