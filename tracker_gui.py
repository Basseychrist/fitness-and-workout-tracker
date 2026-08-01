import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from tracker import (
    create_profile,
    list_profiles,
    create_workout,
    list_workouts,
    update_workout,
    delete_workout,
    update_profile,
    delete_profile,
    format_profile,
    format_workout,
)


class FitnessTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fitness & Workout Tracker")
        self.geometry("760x620")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.profile_tab = ttk.Frame(notebook)
        self.workout_tab = ttk.Frame(notebook)
        notebook.add(self.profile_tab, text="Profiles")
        notebook.add(self.workout_tab, text="Workouts")

        self.status_label = tk.Label(self, text="Ready", anchor="w")
        self.status_label.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.create_profile_tab()
        self.create_workout_tab()

    def create_profile_tab(self):
        frame = ttk.Frame(self.profile_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.profile_name = ttk.Entry(frame, width=40)
        self.profile_name.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky=tk.W)
        self.profile_age = ttk.Entry(frame, width=20)
        self.profile_age.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frame, text="Weight (kg):").grid(row=2, column=0, sticky=tk.W)
        self.profile_weight = ttk.Entry(frame, width=20)
        self.profile_weight.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(frame, text="Goals:").grid(row=3, column=0, sticky=tk.W)
        self.profile_goals = ttk.Entry(frame, width=40)
        self.profile_goals.grid(row=3, column=1, sticky=tk.W)

        create_button = ttk.Button(frame, text="Create Profile", command=self.create_profile_action)
        create_button.grid(row=4, column=0, columnspan=2, pady=10)

        list_button = ttk.Button(frame, text="Refresh Profile List", command=self.refresh_profiles)
        list_button.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(frame, text="Profile ID to update/delete:").grid(row=7, column=0, sticky=tk.W)
        self.edit_profile_id = ttk.Entry(frame, width=40)
        self.edit_profile_id.grid(row=7, column=1, sticky=tk.W)

        update_button = ttk.Button(frame, text="Update Profile", command=self.update_profile_action)
        update_button.grid(row=8, column=0, pady=10)

        delete_button = ttk.Button(frame, text="Delete Profile", command=self.delete_profile_action)
        delete_button.grid(row=8, column=1, pady=10)

        self.profile_output = scrolledtext.ScrolledText(frame, width=85, height=12, wrap=tk.WORD)
        self.profile_output.grid(row=9, column=0, columnspan=2, pady=(10, 0))

        frame.grid_columnconfigure(1, weight=1)

        self.refresh_profiles()

    def create_workout_tab(self):
        frame = ttk.Frame(self.workout_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Profile ID:").grid(row=0, column=0, sticky=tk.W)
        self.workout_profile_id = ttk.Entry(frame, width=40)
        self.workout_profile_id.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
        self.workout_date = ttk.Entry(frame, width=40)
        self.workout_date.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(frame, text="Workout Type:").grid(row=2, column=0, sticky=tk.W)
        self.workout_type = ttk.Entry(frame, width=40)
        self.workout_type.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(frame, text="Duration (minutes):").grid(row=3, column=0, sticky=tk.W)
        self.workout_duration = ttk.Entry(frame, width=40)
        self.workout_duration.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(frame, text="Calories Burned:").grid(row=4, column=0, sticky=tk.W)
        self.workout_calories = ttk.Entry(frame, width=40)
        self.workout_calories.grid(row=4, column=1, sticky=tk.W)

        create_button = ttk.Button(frame, text="Create Workout", command=self.create_workout_action)
        create_button.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(frame, text="Filter by Workout Type:").grid(row=7, column=0, sticky=tk.W)
        self.filter_type = ttk.Entry(frame, width=40)
        self.filter_type.grid(row=7, column=1, sticky=tk.W)

        ttk.Label(frame, text="Filter by Profile ID:").grid(row=8, column=0, sticky=tk.W)
        self.filter_profile_id = ttk.Entry(frame, width=40)
        self.filter_profile_id.grid(row=8, column=1, sticky=tk.W)

        list_button = ttk.Button(frame, text="Refresh Workout List", command=self.refresh_workouts)
        list_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.workout_output = scrolledtext.ScrolledText(frame, width=85, height=12, wrap=tk.WORD)
        self.workout_output.grid(row=10, column=0, columnspan=2, pady=(0, 10))

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=11, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(frame, text="Workout ID to update/delete:").grid(row=12, column=0, sticky=tk.W)
        self.edit_workout_id = ttk.Entry(frame, width=40)
        self.edit_workout_id.grid(row=12, column=1, sticky=tk.W)

        ttk.Label(frame, text="New Duration (minutes):").grid(row=13, column=0, sticky=tk.W)
        self.edit_duration = ttk.Entry(frame, width=40)
        self.edit_duration.grid(row=13, column=1, sticky=tk.W)

        ttk.Label(frame, text="New Calories Burned:").grid(row=14, column=0, sticky=tk.W)
        self.edit_calories = ttk.Entry(frame, width=40)
        self.edit_calories.grid(row=14, column=1, sticky=tk.W)

        update_button = ttk.Button(frame, text="Update Workout", command=self.update_workout_action)
        update_button.grid(row=15, column=0, pady=10)

        delete_button = ttk.Button(frame, text="Delete Workout", command=self.delete_workout_action)
        delete_button.grid(row=15, column=1, pady=10)

        frame.grid_columnconfigure(1, weight=1)
        self.refresh_workouts()

    def set_status(self, message: str, error: bool = False):
        self.status_label.config(text=message, fg="red" if error else "black")

    def create_profile_action(self):
        name = self.profile_name.get().strip()
        if not name:
            messagebox.showwarning("Missing value", "Name is required.")
            return
        age = self.profile_age.get().strip()
        weight = self.profile_weight.get().strip()
        goals = self.profile_goals.get().strip() or None

        try:
            age_val = int(age) if age else None
            weight_val = float(weight) if weight else None
            profile_id = create_profile(name, age_val, weight_val, goals)
            self.set_status(f"Profile created: {profile_id}")
            self.refresh_profiles()
        except ValueError:
            messagebox.showerror("Invalid value", "Age and weight must be numeric.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to create profile.", error=True)

    def update_profile_action(self):
        profile_id = self.edit_profile_id.get().strip()
        if not profile_id:
            messagebox.showwarning("Missing value", "Profile ID is required.")
            return
        updates = {}
        name = self.profile_name.get().strip()
        age = self.profile_age.get().strip()
        weight = self.profile_weight.get().strip()
        goals = self.profile_goals.get().strip()
        if name:
            updates["name"] = name
        if age:
            try:
                updates["age"] = int(age)
            except ValueError:
                messagebox.showerror("Invalid value", "Age must be numeric.")
                return
        if weight:
            try:
                updates["weight_kg"] = float(weight)
            except ValueError:
                messagebox.showerror("Invalid value", "Weight must be numeric.")
                return
        if goals:
            updates["goals"] = goals
        if not updates:
            messagebox.showwarning("No changes", "Enter at least one value to update.")
            return
        try:
            update_profile(profile_id, updates)
            self.set_status("Profile updated.")
            self.refresh_profiles()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to update profile.", error=True)

    def delete_profile_action(self):
        profile_id = self.edit_profile_id.get().strip()
        if not profile_id:
            messagebox.showwarning("Missing value", "Profile ID is required.")
            return
        if not messagebox.askyesno("Confirm", "Delete this profile?"):
            return
        try:
            delete_profile(profile_id)
            self.set_status("Profile deleted.")
            self.refresh_profiles()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to delete profile.", error=True)

    def refresh_profiles(self):
        self.profile_output.delete(1.0, tk.END)
        try:
            profiles = list_profiles()
            if not profiles:
                self.profile_output.insert(tk.END, "No profiles found.\n")
                return
            for p in profiles:
                self.profile_output.insert(tk.END, format_profile(p) + "\n")
            self.set_status("Profile list refreshed.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to refresh profiles.", error=True)

    def create_workout_action(self):
        profile_id = self.workout_profile_id.get().strip()
        if not profile_id:
            messagebox.showwarning("Missing value", "Profile ID is required.")
            return
        date_text = self.workout_date.get().strip() or datetime.date.today().isoformat()
        workout_type = self.workout_type.get().strip()
        if not workout_type:
            messagebox.showwarning("Missing value", "Workout type is required.")
            return
        duration = self.workout_duration.get().strip()
        calories = self.workout_calories.get().strip()

        try:
            duration_val = float(duration)
            calories_val = float(calories)
            workout_id = create_workout(profile_id, date_text, workout_type, duration_val, calories_val)
            self.set_status(f"Workout created: {workout_id}")
            self.refresh_workouts()
        except ValueError:
            messagebox.showerror("Invalid value", "Duration and calories must be numeric.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to create workout.", error=True)

    def refresh_workouts(self):
        self.workout_output.delete(1.0, tk.END)
        try:
            filter_type = self.filter_type.get().strip() or None
            profile_id = self.filter_profile_id.get().strip() or None
            workouts = list_workouts(filter_type, profile_id)
            if not workouts:
                self.workout_output.insert(tk.END, "No workouts found.\n")
                return
            for w in workouts:
                self.workout_output.insert(tk.END, format_workout(w) + "\n")
            self.set_status("Workout list refreshed.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to refresh workouts.", error=True)

    def update_workout_action(self):
        workout_id = self.edit_workout_id.get().strip()
        if not workout_id:
            messagebox.showwarning("Missing value", "Workout ID is required.")
            return
        updates = {}
        duration = self.edit_duration.get().strip()
        calories = self.edit_calories.get().strip()
        if duration:
            try:
                updates["duration_minutes"] = float(duration)
            except ValueError:
                messagebox.showerror("Invalid value", "Duration must be numeric.")
                return
        if calories:
            try:
                updates["calories_burned"] = float(calories)
            except ValueError:
                messagebox.showerror("Invalid value", "Calories must be numeric.")
                return
        if not updates:
            messagebox.showwarning("No changes", "Enter at least one value to update.")
            return
        try:
            update_workout(workout_id, updates)
            self.set_status("Workout updated.")
            self.refresh_workouts()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to update workout.", error=True)

    def delete_workout_action(self):
        workout_id = self.edit_workout_id.get().strip()
        if not workout_id:
            messagebox.showwarning("Missing value", "Workout ID is required.")
            return
        if not messagebox.askyesno("Confirm", "Delete this workout?"):
            return
        try:
            delete_workout(workout_id)
            self.set_status("Workout deleted.")
            self.refresh_workouts()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.set_status("Failed to delete workout.", error=True)


if __name__ == "__main__":
    app = FitnessTrackerGUI()
    app.mainloop()
