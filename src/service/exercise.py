
from model.muscle_group import ExerciseCreate, ExerciseUpdate
from data.exercise import Exercise
from sqlalchemy.orm import Session


def in_db(db: Session, name: str) -> bool:
    if db.query(Exercise).filter(Exercise.name == name).first():
        return True
    return False

def create(db: Session, exercise: ExerciseCreate):
    if in_db(db, exercise.name):
        raise ValueError(f"Упражнение '{exercise.name}' уже существует")

    exercise_db = Exercise(
        name=exercise.name,
        description=exercise.description,
        muscle_group_id=exercise.muscle_group_id
    )
    db.add(exercise_db)
    db.commit()
    db.refresh(exercise_db)
    return exercise_db

def get_all(db: Session) -> list[Exercise]:
    return db.query(Exercise).all()

def get_one(db: Session, exercise_id: int) -> Exercise | None:
    return db.query(Exercise).filter(Exercise.id == exercise_id).filter()

def updade(db: Session, exercise_id: int, update_exercise: ExerciseUpdate) -> Exercise | None:
    exercise_db = get_one(db, exercise_id)
    if not exercise_db:
        return None

    data = update_exercise.model_dump()

    for field, value in data.items():
        if field == "name" and value != exercise_db.name and in_db(db, value):
            raise ValueError(f"Упражнение с названием '{value}' уже существует")
        setattr(exercise_db, field, value)

    db.commit()
    db.refresh(exercise_db)
    return exercise_db

def delete(db: Session, exercise_id: int) -> bool:
    exercise_db = get_one(db, exercise_id)
    if not exercise_db:
        return False

    db.delete(exercise_db)
    db.commit()
    return True
