from models import session, Workout


def welcome_menu():
    print("Welcome to the Workout Program App")
    print("1. Create a new workout program")
    print("2. View saved workout programs")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice


def create_program():
    while True:  # This loop allows the user to go back to the main menu at any point.
        print("Press 'b' to go back to the main menu.")
        cycle_duration = input("Enter Cycle Duration in weeks or type 'Repeating': ")
        if cycle_duration.lower() == 'b':
            break  # Break out of the loop to go back to the main menu.
        frequency = input("Enter Frequency per week (number of workout days): ")
        if frequency.lower() == 'b':
            break  # Break out of the loop to go back to the main menu.
        # Store the input data into the database (to be implemented)
        # Proceed to the next page (to be implemented)


def add_workout():
    name = input("Enter the name of the workout: ")
    new_workout = Workout(name=name)
    session.add(new_workout)
    session.commit()
    print(f"Workout {name} added.")


def view_workouts():
    workouts = session.query(Workout).all()
    for workout in workouts:
        print(f"{workout.id}. {workout.name}")


if __name__ == "__main__":
    while True:
        choice = welcome_menu()
        if choice == '1':
            add_workout()
        elif choice == '2':
            view_workouts()  # Function to view saved programs (to be implemented)
        elif choice == '3':
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")
