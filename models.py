from sqlalchemy import create_engine, Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Database setup
engine = create_engine("sqlite:///workout_programs.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the WorkoutPlan class
class WorkoutPlan(Base):
    """Represents a workout program."""
    __tablename__ = 'workout_plans'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    frequency_days = Column(Integer, nullable=False)

    weeks = relationship('Week', back_populates='workout_plan')

class Week(Base):
    """Represents a week within a workout program."""
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    week_number = Column(Integer, nullable=False)
    workout_plan_id = Column(Integer, ForeignKey('workout_plans.id'), nullable=False)

    workout_plan = relationship('WorkoutPlan', back_populates='weeks')
    days = relationship('Day', back_populates='week')

class Day(Base):
    """Represents a day within a week of a workout program."""
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True)
    day_number = Column(Integer, nullable=False)
    week_id = Column(Integer, ForeignKey('weeks.id'), nullable=False)

    week = relationship('Week', back_populates='days')
    exercises = relationship('Exercise', back_populates='day')

class Exercise(Base):
    """Represents an exercise for a specific day in a workout program."""
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercise_number = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    exercise_type = Column(Integer, nullable=True)
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)

    day = relationship('Day', back_populates='exercises')

    weight = Column(Double)
    notes = Column(String)

Base.metadata.create_all(engine)
