from datetime import datetime, timedelta
from typing import Optional

import jwt

from src.config import pwd_context, settings, TOKEN_ENCODING_ALGORITHM


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, time_delta: Optional[timedelta]):
    to_encode = data.copy()

    expire = datetime.utcnow() + time_delta

    to_encode.update(
        {"exp": expire}
    )
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=TOKEN_ENCODING_ALGORITHM
    )
