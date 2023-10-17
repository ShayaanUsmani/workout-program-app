from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration_weeks = Column(Integer)
    frequency_days = Column(Integer)
    days = relationship('Day', backref='workout')

class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    day_number = Column(Integer)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    exercises = relationship('Exercise', backref='day')

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    day_id = Column(Integer, ForeignKey('days.id'))

DATABASE_URL = "sqlite:///workout.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
