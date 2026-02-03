from model.user import UserLogIn, UserSingUp, UserUpdate
from data.user import User
from sqlalchemy.orm import Session
from core.security import get_password_hash, verify_password

def in_db_name(db: Session, name: str) -> bool:
    if db.query(User).filter(User.username == name).first():
        return True
    return False

def in_db_email(db: Session, email: str) -> bool:
    if db.query(User).filter(User.email == email).first():
        return True
    return False

def singup(db: Session, user: UserSingUp) -> User:
    if in_db_name(db, user.username):
        raise ValueError(f"Пользователь с именем '{user.username}' уже существует")

    if in_db_email(db, user.email):
        raise ValueError(f"Пользователь с почтой '{user.email}' уже существует")

    password_hash = get_password_hash(user.password)

    user_db = User(
        email=user.email,
        username=user.username,
        hashed_password=password_hash,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def get_all(db: Session) -> list[User]:
    return db.query(User).all()

def get_one(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def update(db: Session, user_id: int, update_user: UserUpdate) -> User | None:
    user_db = get_one(db, user_id)
    if not user_db:
        return None

    data = update_user.model_dump()

    if "password" in data:
        data["password"] = get_password_hash(data.pop("password"))

    for field, value in data.items():
        if field == "username" and value != user_db.username and in_db_name(db, value):
            raise ValueError(f"Пользователь с именем '{value}' уже существует")
        if field == "email" and value != user_db.email and in_db_email(db, value):
            raise ValueError(f"Почта '{value}' уже используется")
        setattr(user_db, field, value)

    db.commit()
    db.refresh(user_db)
    return user_db

def delete(db: Session, user_id: int) -> bool:
    user_db = get_one(db, user_id)
    if not user_db:
        return False

    db.delete(user_db)
    db.commit()
    return True

def auth(db: Session, user: UserLogIn) -> User | None:
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise ValueError(f"Пользователь с почтой '{user.email}' не найден")

    if not verify_password(user.password, user_db.hashed_password):
        return None
    return user_db