from fastapi import APIRouter, Depends, HTTPException
from model.muscle_group import MuscleGroup, MuscleGroupCreate, MuscleGroupUpdate
import service.muscle_group as service
from sqlalchemy.orm import Session
from dependencies import get_db


router = APIRouter(prefix = "/muscle_group")

@router.get("/", tags=["Группы мышц"], summary="Получить все группы мышц", response_model=list[MuscleGroup])
def get_all(db: Session = Depends(get_db)) -> list[MuscleGroup]:
    return service.get_all(db)

@router.get("/{id}", tags=["Группы мышц"], summary="Получить одну группу по id")
def get_one(id: int, db: Session = Depends(get_db)) -> MuscleGroup | None:
    db_muscle_group = service.get_one(db, id)
    if db_muscle_group is None:
        raise HTTPException(status_code=404, detail="Группа мышц не найдена")
    return db_muscle_group


@router.post("/", tags=["Группы мышц"], summary="Создать группу мышц")
def create(muscle_group: MuscleGroupCreate, db: Session = Depends(get_db)) -> MuscleGroup:
    return service.create(db, muscle_group)

@router.patch("/", tags=["Группы мышц"], summary="Изменить группу мышц")
def modify(id: int, muscle_group: MuscleGroupUpdate, db: Session = Depends(get_db)) -> MuscleGroup:
    return service.update(db, id, muscle_group)

@router.delete("/{id}", tags=["Группы мышц"], summary="Удалить группу мышц")
def delete(id: int, db: Session = Depends(get_db)) -> bool:
    if not service.delete(db, id):
        raise HTTPException(status_code=404, detail="Группа мышц не найдена")
    return True