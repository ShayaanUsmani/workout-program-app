from models import session, Workout, Exercise, Day

# -------------------------data---------------------------------#
COMPOUND = 1
ACCESSORY = 2
MOBILITY = 3
CARDIO = 4

compound_exercises = ['Bench Press', 'Squat', 'Deadlift', 'Overhead Press', 'Lat Pull Down', 'Cable Row']
accessory_exercises = ['Lateral Raise', 'Bicep Curl', 'Tricep Pushdown', 'Overhead Tricep Extension', 'Rear Delt Fly',
                       'Leg Curl', 'Leg Extension', 'Calf Raises']
mobility_exercises = ['Something']
cardio_exercises = ['Treadmill', 'Bike']


# ----------------------functions-------------------------------#

def welcome_menu():
    print("Welcome to the Workout Program App")
    print("1. Create a new workout program")
    print("2. View saved workout programs")
    print("3. Exit")
    choice = input("\nChoose from 1-3: ")
    if choice == '1':
        add_workout_program()
    elif choice == '2':
        view_workouts()
    elif choice == '3':
        exit()
    else:
        print("Invalid choice. Please try again.")


def add_exercise(exercise_list):
    print()
    for i in range(len(exercise_list)):
        print(str(i + 1) + ". " + exercise_list[i])
    print()
    while True:
        try:
            choice = int(input("Choose from 1-" + str(len(exercise_list)) + ": "))
            if not (1 <= choice <= len(exercise_list)):
                raise ValueError

            exercise_name = exercise_list[choice - 1]

            if exercise_list is cardio_exercises:
                sets = 1
                reps = int(input("How long (in minutes) for " + exercise_name + "? "))
            else:
                sets = int(input("How many sets of " + exercise_name + "? "))
                reps = int(input("How many reps per set? "))
            break

        except ValueError:
            print("Invalid entry, please try again")

    return Exercise(name=exercise_list[choice - 1], sets=sets, reps=reps)


def add_workout_program():
    workout_name = input("\nEnter the name of the workout: ")
    duration = int(input("Enter Cycle Duration in weeks (number of weeks in program): "))
    frequency = int(input("Enter Frequency per week (number of workout days per week): "))

    # Create a new Workout instance
    new_workout = Workout(name=workout_name, duration_weeks=duration, frequency_days=frequency)
    session.add(new_workout)
    session.commit()

    # Loop through the number of days and allow user to add exercises for each day
    for day_num in range(1, frequency + 1):
        print("\nDay " + str(day_num))
        new_day = Day(day_number=day_num, workout=new_workout)
        session.add(new_day)
        while True:
            print("1. Add compound/main movement")
            print("2. Add accessory/isolation movement")
            print("3. Add mobility movement")
            print("4. Add cardio")
            print("5. Next day")
            print("6. Exit")

            choice = input("\nChoose from 1-6: ")

            if choice == "1":
                new_exercise = add_exercise(compound_exercises)
            elif choice == "2":
                new_exercise = add_exercise(accessory_exercises)
            elif choice == "3":
                new_exercise = add_exercise(mobility_exercises)
            elif choice == "4":
                new_exercise = add_exercise(cardio_exercises)
            elif choice == "5":
                break
            elif choice == "6":
                return

            new_exercise.day_id = new_day.id
            session.add(new_exercise)
        session.commit()


def view_workouts():
    workouts = session.query(Workout).all()
    for workout in workouts:
        print(str(workout.id) + ". " + workout.name)


# -------------------------MAIN--------------------------------------------#
welcome_menu()
