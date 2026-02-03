from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False

class UserSingUp(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None
    username: str | None
    password: str | None
    is_active: bool | None
    is_superuser: bool | None

class User(UserBase):
    id: int

class UserLogIn(BaseModel):
    email: EmailStr
    password: str

# Схемы для аутентификации
class Token(BaseModel):
    """Схема для JWT токена"""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Схема для данных в токене"""
    sub: int | None

class LoginRequest(BaseModel):
    """Схема для запроса логина"""
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    """Схема для запроса регистрации"""
    email: EmailStr
    username: str
    password: str