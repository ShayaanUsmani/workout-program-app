from models import session, Workout

def add_workout():
    name = input("Enter the name of the workout: ")
    new_workout = Workout(name=name)
    session.add(new_workout)
    session.commit()
    print(f"Workout {name} added.")

add_workout()

def view_workouts():
    workouts = session.query(Workout).all()
    for workout in workouts:
        print(f"{workout.id}. {workout.name}")

view_workouts()
