from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base
import datetime

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)
    exercises = relationship("Exercise", back_populates="workout")
    ass_exercises = relationship("AssExercise", back_populates="workout")
    user = relationship("User", back_populates="workouts")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "<Workout {}>".format(self.name)