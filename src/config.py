from typing import Any, Optional

from passlib.context import CryptContext

from pydantic.env_settings import BaseSettings
from starlette.config import Config


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: Optional[str]
    ORIGINS: Optional[str]
    TEST_SQLALCHEMY_DATABASE_URI: Optional[str]

    class Config:
        env_file = ".env"


settings = Settings()
config= Config(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_LIFETIME: int = 30

TOKEN_ENCODING_ALGORITHM: str = "HS256"