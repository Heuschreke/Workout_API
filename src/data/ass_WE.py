from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from data.database import Base

class AssExercise(Base):
    __tablename__ = "ass_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout = relationship("Workout", back_populates="ass_exercises")
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    exercise = relationship("Exercise", back_populates="ass_exercises")
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    __table_args__ = (UniqueConstraint("workout_id", "exercise_id", name='uq_ass_exercise'))

    sets = Column(Integer, default=3)
    reps = Column(Integer, default=8)
    weight = Column(Integer, nullable=True)
    rest_time = Column(Integer, default=60)
