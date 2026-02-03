from fastapi import APIRouter, Depends, HTTPException
from model.muscle_group import Exercise, ExerciseCreate, ExerciseUpdate
import service.exercise as service
from sqlalchemy.orm import Session
from dependencies import get_db


router = APIRouter(prefix = "/exercise")

@router.get("/", tags=["Упражнения"], summary="Получить все упражнения", response_model=list[Exercise])
def get_all(db: Session = Depends(get_db)) -> list[Exercise]:
    return service.get_all(db)

@router.get("/{id}", tags=["Упражнения"], summary="Получить одно упражнение по id")
def get_one(id: int, db: Session = Depends(get_db)) -> Exercise | None:
    db_exercise = service.get_one(db, id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    return db_exercise


@router.post("/", tags=["Упражнения"], summary="Создать новое упражнение")
def create(exercise: ExerciseCreate, db: Session = Depends(get_db)) -> Exercise:
    return service.create(db, exercise)

@router.patch("/", tags=["Упражнения"], summary="Изменить упражнение")
def modify(id: int, exercise: ExerciseUpdate, db: Session = Depends(get_db)) -> Exercise:
    return service.update(db, id, exercise)

@router.delete("/{id}", tags=["Упражнения"], summary="Удалить упражнение")
def delete(id: int, db: Session = Depends(get_db)) -> bool:
    if not service.delete(db, id):
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    return True