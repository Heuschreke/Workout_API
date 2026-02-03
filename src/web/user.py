# src/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import settings

from dependencies import get_current_active_user, get_current_superuser
from data.database import get_db
from model.user import User, UserSingUp, UserUpdate
from service import user

router = APIRouter(prefix=f"{settings.API_V1_STR}/users", tags=["users"])

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Получить информацию о текущем пользователе"""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить информацию о текущем пользователе"""
    try:
        updated_user = user.update(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)  # Только для админов
):
    """Получить список пользователей (только для админов)"""
    users = user.get_all(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)  # Только для админов
):
    """Получить пользователя по ID (только для админов)"""
    user_ = user.get_one(db, user_id)
    if user_ is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_