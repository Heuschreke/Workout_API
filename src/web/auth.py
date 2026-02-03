# src/api/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token
from data.database import get_db
from model.user import Token, RegisterRequest, User
from service import user

router = APIRouter(prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Логин пользователя"""
    user_ = user.auth(
        db, email=form_data.username, password=form_data.password
    )

    if not user_:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    try:
        # Преобразуем RegisterRequest в UserCreate
        from ..model.user import UserSingUp
        user_create = UserSingUp(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )

        user = user.singup(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """Выход пользователя (на клиенте нужно удалить токен)"""
    return {"message": "Successfully logged out"}