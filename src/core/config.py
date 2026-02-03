# src/core/config.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Базовые настройки
    PROJECT_NAME: str = "Fitness Tracker API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Настройки базы данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fitness.db")

    # Настройки JWT
    SECRET_KEY: str = os.getenv("maximum_power")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 часа

    # Настройки CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()