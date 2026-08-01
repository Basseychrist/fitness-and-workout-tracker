"""Firestore-backed fitness tracker logic for profiles and workouts."""

import datetime
from typing import List, Dict, Optional

from firebase_config import db


# Firestore collection names used for high-level profile and workout storage.
PROFILES_COLL = "user_profiles"
WORKOUTS_COLL = "workouts"


def create_profile(name: str, age: Optional[int] = None, weight_kg: Optional[float] = None, goals: Optional[str] = None) -> str:
    """Create a new user profile in Firestore and return its document ID.

    Args:
        name: The user's name.
        age: The user's age, if available.
        weight_kg: The user's weight in kilograms, if available.
        goals: The user's fitness goals, if provided.

    Returns:
        The Firestore document ID for the created profile.
    """
    data = {
        "name": name,
        "age": age,
        "weight_kg": weight_kg,
        "goals": goals,
        "created_at": datetime.datetime.utcnow(),
    }
    doc_ref = db.collection(PROFILES_COLL).document()
    doc_ref.set(data)
    return doc_ref.id


def get_profile(profile_id: str) -> Optional[Dict]:
    """Fetch a user profile from Firestore by its document ID.

    Args:
        profile_id: The Firestore document ID for the profile.

    Returns:
        The profile data as a dictionary, or None if the profile does not exist.
    """
    doc = db.collection(PROFILES_COLL).document(profile_id).get()
    if not doc.exists:
        return None
    out = doc.to_dict()
    out["id"] = doc.id
    return out


def list_profiles() -> List[Dict]:
    """List all user profiles stored in Firestore.

    Returns:
        A list of profile dictionaries, each including its document ID.
    """
    docs = db.collection(PROFILES_COLL).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]


def format_profile(profile: Dict) -> str:
    """Format a profile dictionary into a human-readable string.

    Args:
        profile: The profile dictionary to format.

    Returns:
        A formatted multiline string representing the profile.
    """
    created_at = profile.get("created_at")
    created_at_text = created_at.isoformat() if created_at else "N/A"
    return (
        f"Profile ID: {profile.get('id')}\n"
        f"  Name: {profile.get('name')}\n"
        f"  Age: {profile.get('age') or 'N/A'}\n"
        f"  Weight (kg): {profile.get('weight_kg') or 'N/A'}\n"
        f"  Goals: {profile.get('goals') or 'N/A'}\n"
        f"  Created: {created_at_text}\n"
    )


def delete_profile(profile_id: str) -> None:
    """Delete the specified user profile from Firestore.

    Args:
        profile_id: The Firestore document ID for the profile to delete.
    """
    db.collection(PROFILES_COLL).document(profile_id).delete()


def update_profile(profile_id: str, updates: Dict) -> None:
    """Update the specified user profile with the given fields.

    Args:
        profile_id: The Firestore document ID for the profile.
        updates: A dictionary of fields to update.
    """
    db.collection(PROFILES_COLL).document(profile_id).update(updates)


def create_workout(profile_id: str, date: str, workout_type: str, duration_minutes: float, calories_burned: float) -> str:
    """Create a workout record linked to a user profile and return its Firestore ID.

    Args:
        profile_id: The Firestore document ID of the profile that performed the workout.
        date: The workout date, typically in YYYY-MM-DD format.
        workout_type: The type of workout, such as Cardio or Strength.
        duration_minutes: Duration of the workout in minutes.
        calories_burned: Calories burned during the workout.

    Returns:
        The Firestore document ID for the created workout.
    """
    profile_ref = db.collection(PROFILES_COLL).document(profile_id)
    data = {
        "profile_ref": profile_ref,
        "date": date,
        "workout_type": workout_type,
        "duration_minutes": duration_minutes,
        "calories_burned": calories_burned,
        "created_at": datetime.datetime.utcnow(),
    }
    doc_ref = db.collection(WORKOUTS_COLL).document()
    doc_ref.set(data)
    return doc_ref.id


def get_workout(workout_id: str) -> Optional[Dict]:
    """Fetch a workout record by its Firestore document ID.

    Args:
        workout_id: The Firestore document ID for the workout.

    Returns:
        The workout data dictionary including the profile ID, or None if not found.
    """
    doc = db.collection(WORKOUTS_COLL).document(workout_id).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    # convert reference to id for readability
    profile_ref = data.get("profile_ref")
    data["profile_id"] = profile_ref.id if profile_ref else None
    data["id"] = doc.id
    return data


def list_workouts(filter_type: Optional[str] = None, profile_id: Optional[str] = None) -> List[Dict]:
    """List workouts, optionally filtering by type or profile.

    Args:
        filter_type: Filter workouts by the workout_type field.
        profile_id: Filter workouts by user profile ID.

    Returns:
        A list of workout dictionaries, each including its document ID and profile ID.
    """
    query = db.collection(WORKOUTS_COLL)
    if filter_type:
        query = query.where("workout_type", "==", filter_type)
    if profile_id:
        profile_ref = db.collection(PROFILES_COLL).document(profile_id)
        query = query.where("profile_ref", "==", profile_ref)
    docs = query.stream()
    out = []
    for d in docs:
        data = d.to_dict()
        profile_ref = data.get("profile_ref")
        data["profile_id"] = profile_ref.id if profile_ref else None
        data["id"] = d.id
        out.append(data)
    return out


def format_workout(workout: Dict) -> str:
    """Format a workout dictionary into a readable string.

    Args:
        workout: The workout dictionary to format.

    Returns:
        A formatted multiline string representing the workout.
    """
    return (
        f"Workout ID: {workout.get('id')}\n"
        f"  Profile ID: {workout.get('profile_id') or 'N/A'}\n"
        f"  Date: {workout.get('date') or 'N/A'}\n"
        f"  Type: {workout.get('workout_type') or 'N/A'}\n"
        f"  Duration: {workout.get('duration_minutes') or 'N/A'} minutes\n"
        f"  Calories: {workout.get('calories_burned') or 'N/A'}\n"
    )


def update_workout(workout_id: str, updates: Dict) -> None:
    """Update a workout record with the given fields.

    Args:
        workout_id: The Firestore document ID for the workout.
        updates: A dictionary of fields to update.
    """
    db.collection(WORKOUTS_COLL).document(workout_id).update(updates)


def delete_workout(workout_id: str) -> None:
    """Delete the specified workout from Firestore.

    Args:
        workout_id: The Firestore document ID for the workout to delete.
    """
    db.collection(WORKOUTS_COLL).document(workout_id).delete()


def prompt_float(prompt: str) -> float:
    """Prompt the user for a floating-point number and retry until valid input is entered.

    Args:
        prompt: The input prompt string displayed to the user.

    Returns:
        The value entered by the user as a float.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def cli_menu():
    """Run the main command-line menu for the fitness tracker.

    The menu allows users to create, list, update, and delete profiles and workouts.
    """
    while True:
        print("\nFitness & Workout Tracker")
        print("1) Create user profile")
        print("2) List user profiles")
        print("3) Update user profile")
        print("4) Delete user profile")
        print("5) Create workout")
        print("6) List workouts")
        print("7) Update workout")
        print("8) Delete workout")
        print("9) Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Name: ")
            age = input("Age (optional): ")
            weight = input("Weight kg (optional): ")
            goals = input("Goals (optional): ")
            age_val = int(age) if age.strip() else None
            weight_val = float(weight) if weight.strip() else None
            pid = create_profile(name, age_val, weight_val, goals or None)
            print(f"Created profile id: {pid}")

        elif choice == "2":
            profiles = list_profiles()
            if not profiles:
                print("No profiles found.")
            for p in profiles:
                print(format_profile(p))

        elif choice == "3":
            pid = input("Profile ID to update: ")
            print("Enter new values (leave blank to skip):")
            name = input("Name: ")
            age = input("Age: ")
            weight = input("Weight kg: ")
            goals = input("Goals: ")
            updates = {}
            if name.strip():
                updates["name"] = name
            if age.strip():
                updates["age"] = int(age)
            if weight.strip():
                updates["weight_kg"] = float(weight)
            if goals.strip():
                updates["goals"] = goals
            if updates:
                update_profile(pid, updates)
                print("Profile updated.")
            else:
                print("No updates provided.")

        elif choice == "4":
            pid = input("Profile ID to delete: ")
            delete_profile(pid)
            print("Profile deleted.")

        elif choice == "5":
            profile_id = input("Profile ID: ")
            date = input("Date (YYYY-MM-DD) or leave blank for today: ")
            if not date.strip():
                date = datetime.date.today().isoformat()
            wtype = input("Workout Type (e.g., Cardio, Strength): ")
            duration = prompt_float("Duration minutes: ")
            calories = prompt_float("Calories burned: ")
            wid = create_workout(profile_id, date, wtype, duration, calories)
            print(f"Created workout id: {wid}")

        elif choice == "6":
            ftype = input("Filter by workout type (blank for all): ")
            pid = input("Filter by profile id (blank for all): ")
            ftype = ftype.strip() or None
            pid = pid.strip() or None
            workouts = list_workouts(ftype, pid)
            if not workouts:
                print("No workouts found.")
            for w in workouts:
                print(format_workout(w))

        elif choice == "7":
            wid = input("Workout ID to update: ")
            print("Enter new values (leave blank to skip):")
            duration = input("Duration minutes: ")
            calories = input("Calories burned: ")
            updates = {}
            if duration.strip():
                updates["duration_minutes"] = float(duration)
            if calories.strip():
                updates["calories_burned"] = float(calories)
            if updates:
                update_workout(wid, updates)
                print("Workout updated.")
            else:
                print("No updates provided.")

        elif choice == "8":
            # Delete a workout record by ID.
            wid = input("Workout ID to delete: ")
            delete_workout(wid)
            print("Workout deleted.")

        elif choice == "9":
            # Exit the CLI loop and terminate the program.
            print("Goodbye")
            break

        else:
            # Handle invalid menu selections.
            print("Unknown option, try again.")


# When the file is run directly, start the command-line interface.
if __name__ == "__main__":
    cli_menu()
