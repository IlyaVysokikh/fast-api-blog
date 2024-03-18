from datetime import timedelta, datetime
from typing import Any, Generator, Optional

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from jose import jwt

from src.config import pwd_context, settings, TOKEN_ENCODING_ALGORITHM
from src.models.user import UserModel
from src.repository.session import SessionLocal




def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


#TODO Авторизация!!!
def get_current_user(db: Session = Depends(),
                     token: str = Depends(),
                     credentials_exception=HTTPException(
                         status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={
                             "WWW-Authenticate": "Bearer"
                         }
    )):
    ...


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive"
        )
    return current_user


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
