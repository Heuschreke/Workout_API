from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id"), index=True, nullable=True)
    muscle_group = relationship("MuscleGroup", back_populates="exercises")
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=True)
    workout = relationship("Workout", back_populates="exercises")

    def __repr__(self):
        return "<Exercise {}>".format(self.name)