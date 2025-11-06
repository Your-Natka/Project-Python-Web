from pydantic_settings import BaseSettings
import cloudinary
from typing import ClassVar
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "mydatabase"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/mydatabase"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    CLOUDINARY_URL: ClassVar[str] = "cloudinary://API_KEY:API_SECRET@CLOUD_NAME"


    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()