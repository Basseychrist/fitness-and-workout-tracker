import datetime
from typing import List, Dict, Optional

from firebase_config import db


# Collections
PROFILES_COLL = "user_profiles"
WORKOUTS_COLL = "workouts"


def create_profile(name: str, age: Optional[int] = None, weight_kg: Optional[float] = None, goals: Optional[str] = None) -> str:
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
    doc = db.collection(PROFILES_COLL).document(profile_id).get()
    if not doc.exists:
        return None
    out = doc.to_dict()
    out["id"] = doc.id
    return out


def list_profiles() -> List[Dict]:
    docs = db.collection(PROFILES_COLL).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]


def format_profile(profile: Dict) -> str:
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
    db.collection(PROFILES_COLL).document(profile_id).delete()


def update_profile(profile_id: str, updates: Dict) -> None:
    db.collection(PROFILES_COLL).document(profile_id).update(updates)


def create_workout(profile_id: str, date: str, workout_type: str, duration_minutes: float, calories_burned: float) -> str:
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
    return (
        f"Workout ID: {workout.get('id')}\n"
        f"  Profile ID: {workout.get('profile_id') or 'N/A'}\n"
        f"  Date: {workout.get('date') or 'N/A'}\n"
        f"  Type: {workout.get('workout_type') or 'N/A'}\n"
        f"  Duration: {workout.get('duration_minutes') or 'N/A'} minutes\n"
        f"  Calories: {workout.get('calories_burned') or 'N/A'}\n"
    )


def update_workout(workout_id: str, updates: Dict) -> None:
    db.collection(WORKOUTS_COLL).document(workout_id).update(updates)


def delete_workout(workout_id: str) -> None:
    db.collection(WORKOUTS_COLL).document(workout_id).delete()


def prompt_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def cli_menu():
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
            wid = input("Workout ID to delete: ")
            delete_workout(wid)
            print("Workout deleted.")

        elif choice == "9":
            print("Goodbye")
            break

        else:
            print("Unknown option, try again.")


if __name__ == "__main__":
    cli_menu()
