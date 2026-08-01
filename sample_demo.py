from tracker import create_profile, create_workout, list_workouts


def demo():
    print("Creating demo profile...")
    pid = create_profile("Demo User", age=30, weight_kg=75.0, goals="Lose fat")
    print("Profile id:", pid)

    print("Logging a workout...")
    wid = create_workout(pid, date="2026-07-31", workout_type="Cardio", duration_minutes=45, calories_burned=350)
    print("Workout id:", wid)

    print("Listing workouts for profile...")
    workouts = list_workouts(profile_id=pid)
    for w in workouts:
        print(w)


if __name__ == "__main__":
    demo()
