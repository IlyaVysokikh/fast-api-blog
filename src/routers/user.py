from datetime import timedelta
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from starlette import status

from src import schemas
from src.config import TOKEN_LIFETIME
from src.services.depends import get_db, get_current_active_user, create_access_token
from src.services.user import (
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    update_user, authenticate_user
)

router = APIRouter(
    tags=[
        "users"
    ]
)


@router.post("/users", response_model=schemas, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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

    return create_user(db=db, user=user)


@router.get("/users/{username}", response_model=schemas)
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


@router.post("/users/login", response_model=schemas)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends()):
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
                     user: schemas.user.UserUpdate,
                     current_user: schemas.User = Depends(get_current_active_user),
                     db: Session = Depends(get_db)
                     ):
    if username != current_user.username:
        raise HTTPException(
            status_code=403,
            detail="You dont have permission"
        )

    return update_user(db, user, username)


