from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from data.database import Base


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    exercises = relationship("Exercise", back_populates="muscle_group")

    def __repr__(self):
        return "<Muscle group {}>".format(self.name)