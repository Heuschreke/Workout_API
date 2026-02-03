# src/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from data.database import SessionLocal
from core.config import settings
from core.security import verify_token
from data.user import User
from model.user import TokenPayload

# OAuth2 схема для получения токена из запроса
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False  # Разрешаем анонимный доступ к некоторым эндпоинтам
)


def get_db():
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Новая функция для получения текущего пользователя (опционально)
async def get_current_user_optional(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Получить текущего пользователя, если токен предоставлен.
    Возвращает None для анонимных пользователей.
    """
    if token is None:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    token_data = TokenPayload(sub=user_id)

    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception

    return user

# Функция для обязательной аутентификации
async def get_current_user(
    current_user: User = Depends(get_current_user_optional),
) -> User:
    """Зависимость для обязательной аутентификации"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

# Функция для проверки активного пользователя
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Зависимость для проверки активного пользователя"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Функция для проверки суперпользователя
async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Зависимость для проверки суперпользователя"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user