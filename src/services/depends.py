from datetime import timedelta, datetime
from typing import Any, Generator, Optional

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

import jwt

from src.config import settings, TOKEN_ENCODING_ALGORITHM, oauth2_scheme
from src.models.user import UserModel
from src.db.session import SessionLocal
from src.services.user import get_user_by_username
from src.schemas.jwt_token import Token, TokenData


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[TOKEN_ENCODING_ALGORITHM]
        )
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except JWTError:  # pragma: no cover
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive"
        )
    return current_user
