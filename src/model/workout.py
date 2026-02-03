from pydantic import BaseModel

class WorkoutBase(BaseModel):
    name: str
    exercises: list

class Workout(WorkoutBase):
    id: int
