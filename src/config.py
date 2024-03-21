from typing import Any, Optional

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from pydantic import BaseConfig, PostgresDsn
from starlette.config import Config


class Settings(BaseConfig):
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = "postgresql://postgres:Qwe272003Qwe!@localhost/blog"
    SECRET_KEY: Optional[str]
    ORIGINS: Optional[str]
    TEST_SQLALCHEMY_DATABASE_URI: Optional[str]

    class Config:
        env_file = ".env"


settings = Settings()
config = Config(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_LIFETIME: int = 30

TOKEN_ENCODING_ALGORITHM: str = "HS256"

oauth2_scheme: Any = OAuth2PasswordBearer(tokenUrl="token")