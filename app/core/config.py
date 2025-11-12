# from pydantic_settings import BaseSettings
# from fastapi.security import OAuth2PasswordBearer
# import cloudinary
# from typing import ClassVar
# import os

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "My FastAPI Project"
#     POSTGRES_USER: str = "postgres"
#     POSTGRES_PASSWORD: str = "password"
#     POSTGRES_SERVER: str = "db"
#     POSTGRES_PORT: str = "5432"
#     POSTGRES_DB: str = "mydatabase"
#     DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/mydatabase"
#     REDIS_URL: str = "redis://localhost:6379/0"
#     SECRET_KEY: str = "supersecretkey"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
#     CLOUDINARY_URL: ClassVar[str] = "cloudinary://API_KEY:API_SECRET@CLOUD_NAME"
#     DATABASE_URL: str = "sqlite:///./test.db"
    
#     # OAuth2 settings
#     oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

#     class Config:
#         env_file = ".env"
#         extra = "ignore"

# settings = Settings()

from os import environ
from pathlib import Path
# from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH_PROJECT = Path(__file__).resolve().parent.parent
BASE_PATH = BASE_PATH_PROJECT.parent
ENV_PATH = BASE_PATH.joinpath(".env")
# assert ENV_PATH.is_file(), f"ENV_PATH must be {ENV_PATH}"
# load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    sqlalchemy_database_url: str | None = None

    mail_username: str = "test@example.com"
    mail_password: str = "SuperStronGPasswrod"
    mail_from: str = "test@example.com"
    mail_port: int = 465
    mail_server: str = "localhost"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    cloudinary_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    app_host: str = "0.0.0.0"
    app_port: int = 9000
    SPHINX_DIRECTORY: str = str(BASE_PATH.joinpath("docs", "_build", "html"))
    STATIC_DIRECTORY: str = str(BASE_PATH.joinpath("static"))

    hcaptcha_enabled: bool = False
    hcaptcha_site_key: str = ""
    hcaptcha_secret_key: str= ""

    model_config = SettingsConfigDict(
        extra="ignore", env_file=str(ENV_PATH), env_file_encoding="utf-8"
    )


settings = Settings()
