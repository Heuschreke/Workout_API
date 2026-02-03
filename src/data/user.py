from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from data.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return "<User {}>".format(self.username)