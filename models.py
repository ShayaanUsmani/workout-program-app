from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the Workout model
Base = declarative_base()
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, Sequence('workout_id_seq'), primary_key=True)
    name = Column(String(100))

# Create an SQLite database in memory
engine = create_engine('sqlite:///workout_program.db')

# Create the table structure
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()
