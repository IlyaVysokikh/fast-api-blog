from datetime import timedelta

from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from starlette import status

from src.schemas.user import *
from src.config import TOKEN_LIFETIME
from src.services.auth import create_access_token
from src.services.depends import get_db, get_current_active_user
from src.services.user import (
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    update_user, authenticate_user,
)
from src.services.user import create_user as create_user_service

router = APIRouter(
    tags=[
        "users"
    ]
)


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_username = get_user_by_username(db, username=user.username)
    db_email = get_user_by_email(db, email=user.email)

    if db_username:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    if db_email:
        raise HTTPException(
            status_code=400,
            detail="email already registered"
        )

    return create_user_service(db=db, user=user)


@router.get("/users/{username}", )
def get_user(username: Optional[str] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if username:
        db_user = get_user_by_username(db, username)
    elif user_id:
        db_user = get_user_by_id(db, user_id)
    else:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db_user


@router.post("/users/login", )
def login(form_data  = Depends(), db  = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
    access_token_lifetime = timedelta(minutes=TOKEN_LIFETIME)
    access_token = create_access_token(
        data={"sub": user},
        time_delta=access_token_lifetime
    )

    return {"access_token": access_token, "token_type": "Bearer"}


@router.put("/users/{username}")
def update_user_data(username: Optional[str],
                     user,
                     current_user = Depends(get_current_active_user),
                     db: Session = Depends(get_db)
                     ):
    if username != current_user.username:
        raise HTTPException(
            status_code=403,
            detail="You dont have permission"
        )

    return update_user(db, user, username)


