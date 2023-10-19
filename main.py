from models import session, WorkoutPlan, Week, Day, Exercise

# ------------------------- Data ------------------------- #

# Constants for exercise types
COMPOUND = 1
ACCESSORY = 2
MOBILITY = 3
CARDIO = 4

# Lists of example exercises for each type
COMPOUND_EXERCISES = ['Bench Press', 'Squat', 'Deadlift', 'Overhead Press', 'Lat Pull Down', 'Cable Row']
ACCESSORY_EXERCISES = ['Lateral Raise', 'Bicep Curl', 'Tricep Pushdown', 'Overhead Tricep Extension', 'Rear Delt Fly',
                       'Leg Curl', 'Leg Extension', 'Calf Raises']
MOBILITY_EXERCISES = ['Something']
CARDIO_EXERCISES = ['Treadmill', 'Bike']


# ------------------------- Functions ------------------------- #

def get_user_input_for_exercise(exercise_name, is_cardio):
    """Get user input for sets and reps (or duration for cardio)."""
    print()
    if is_cardio:
        sets = 1
        reps = int(input(f"How long (in minutes) for {exercise_name}? "))
    else:
        sets = int(input(f"How many sets of {exercise_name}? "))
        reps = int(input("How many reps per set? "))
    return [sets, reps]


def welcome_menu():
    """Display the main welcome menu and handle user choices."""
    print("Welcome to the Workout Program App")
    print("1. Create a new workout program")
    print("2. View saved workout programs")
    print("3. Exit")

    actions = {
        '1': add_workout_program,
        '2': view_workouts,
        '3': exit
    }

    while True:
        choice = input("Choose from 1-3: ")

        action = actions.get(choice)
        if action:
            action()
            break
        else:
            print("Invalid choice. Please try again.")


def add_exercise(exercise_list, new_day_id):
    print()
    for i in range(len(exercise_list)):
        print(f"{i + 1}. {exercise_list[i]}")
    print()

    while True:
        try:
            choice = int(input(f"Choose from 1-{str(len(exercise_list))}: "))
            if not (1 <= choice <= len(exercise_list)):
                raise ValueError

            exercise_name = exercise_list[choice - 1]
            sets_x_reps = get_user_input_for_exercise(exercise_name, exercise_list == CARDIO_EXERCISES)
            new_exercise = Exercise(name=exercise_name, sets=sets_x_reps[0], reps=sets_x_reps[1], day_id=new_day_id)
            session.add(new_exercise)

            break

        except ValueError:
            print("Invalid entry, please try again")
        session.commit()

def add_workout_program():
    """Allow the user to create a new workout program."""
    name = input("Enter the name of the new workout program: ")
    duration_weeks = int(input("How many weeks will this program last? "))
    frequency_days = int(input("How many days per week? "))

    new_workout_plan = WorkoutPlan(name=name, duration_weeks=duration_weeks, frequency_days=frequency_days)
    session.add(new_workout_plan)
    session.commit()

    for week_number in range(1, duration_weeks):
        # Adding the initial week separately so the user only has to input their exercises for one week
        # Data will be copied to other weeks later
        initial_week = Week(week_number=1, workout_plan_id=new_workout_plan.id)
        session.add(initial_week)
        session.commit()

        if week_number == 1:
            for day_number in range(1, frequency_days + 1):
                new_day = Day(day_number=day_number, week_id=initial_week.id)
                session.add(new_day)
                session.commit()
                new_day_id = new_day.id
                while True:
                    print("What type of exercise would you like to add?")
                    print("1. Compound")
                    print("2. Accessory")
                    print("3. Mobility")
                    print("4. Cardio")
                    print("5. Finish Day")
                    print("6. Finish Program")
                    choice = input(f"Choose from 1-6: ")

                    if choice == '1':
                        add_exercise(COMPOUND_EXERCISES, new_day_id)
                    elif choice == '2':
                        add_exercise(ACCESSORY_EXERCISES, new_day_id)
                    elif choice == '3':
                        add_exercise(MOBILITY_EXERCISES, new_day_id)
                    elif choice == '4':
                        add_exercise(CARDIO_EXERCISES, new_day_id)
                    elif choice == '5':
                        break
                    elif choice == '6':
                        return
                    else:
                        print("Invalid choice. Please try again.")
        else:
            new_week = Week(week_number=week_number, workout_plan_id=new_workout_plan.id)
            session.add(new_week)
            session.commit()
            for day_number in range(1, frequency_days + 1):
                new_day = Day(day_number=day_number, week_id=new_week.id)
                session.add(new_day)
                session.commit()
                for exercise in range(initial_week.days.exercises):
                    new_exercise = Exercise(name=exercise.name, sets=exercise.sets, reps=exercise.reps,
                                            day_id=new_day.id)
                    session.add(new_exercise)
                    session.commit()


def view_workouts():
    """View all saved workout programs."""
    workout_plans = session.query(WorkoutPlan).all()
    weeks = session.query(Week).all()
    days = session.query(Day).all()
    exercises = session.query(Exercise).all()
    if not workout_plans:
        print("No workout programs found.")
        return

    print("Saved Workout Programs:")
    for i, workout_plan in enumerate(workout_plans, start=1):
        print(f"{i}. {workout_plan.name}")

    choice = int(input(f"Choose from 1-{len(workout_plans)}: "))
    if 1 <= choice <= len(workout_plans):
        for week in weeks:
            print(f"Week {week.week_number}")
            for day in days:
                print(f"Day {day.day_number}")
                for exercise in exercises:
                    print(f"{exercise.name}: {exercise.sets} x {exercise.reps}")



def exit():
    """Exit the program."""
    print("Goodbye!")
    session.close()
    quit()


# ------------------------- Main ------------------------- #

if __name__ == "__main__":
    welcome_menu()
