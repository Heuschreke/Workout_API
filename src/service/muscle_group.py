from model.muscle_group import MuscleGroupCreate, MuscleGroupUpdate
from data.muscle_group import MuscleGroup
from sqlalchemy.orm import Session


def create(db: Session, muscle_group: MuscleGroupCreate):
    if db.query(MuscleGroup).filter(MuscleGroup.name == muscle_group.name).first():
        raise ValueError(f"Группа мышц '{muscle_group.name}' уже существует")

    muscle_group_db = MuscleGroup(
        name=muscle_group.name
    )
    db.add(muscle_group_db)
    db.commit()
    db.refresh(muscle_group_db)
    return muscle_group_db

def get_all(db: Session) -> list[MuscleGroup]:
    return db.query(MuscleGroup).all()

def get_one(db: Session, muscle_group_id: int) -> MuscleGroup | None:
    return db.query(MuscleGroup).filter(MuscleGroup.id == muscle_group_id).first()

def update(db: Session, muscle_group_id: int, update_muscle_group: MuscleGroupUpdate) -> MuscleGroup | None:
    muscle_group_db = get_one(db, muscle_group_id)
    if not muscle_group_db:
        return None

    data = update_muscle_group.model_dump()
    # data = MuscleGroup(name = update_muscle_group.name)
    for field, value in data.items():
        if field == "name" and value != muscle_group_db.name:
            if db.query(MuscleGroup).filter(MuscleGroup.name == value).first():
                raise ValueError(f"Группа мышц с названием '{value}' уже существует")
        setattr(muscle_group_db, field, value)

    db.commit()
    db.refresh(muscle_group_db)
    return muscle_group_db

def delete(db: Session, muscle_group_id: int) -> bool:
    muscle_group_db = get_one(db, muscle_group_id)
    if not muscle_group_db:
        return False

    db.delete(muscle_group_db)
    db.commit()
    return True