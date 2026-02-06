
from pydantic import BaseModel, ConfigDict, Field


class ExerciseBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    description: str | None
    muscle_group_id: int

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseInMuscleGroup(BaseModel):
    name: str

class ExerciseUpdate(BaseModel):
    name: str | None
    description: str | None
    muscle_group_id: int | None

class Exercise(ExerciseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MuscleGroupBase(BaseModel):
    name: str
    
class MuscleGroupUpdate(MuscleGroupBase):
    name: str | None

class MuscleGroupCreate(MuscleGroupBase):
    pass

class MuscleGroup(MuscleGroupBase):
    id: int
    exercises: list[ExerciseInMuscleGroup] = []
