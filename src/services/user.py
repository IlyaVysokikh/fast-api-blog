from typing import Optional

from sqlalchemy.orm import Session

from src import models, schemas
from src.services.depends import get_hashed_password, verify_password


def get_user_by_username(db: Session, username: str) -> Optional[models.UserModel]:
    return db.query(models.UserModel).filter(models.UserModel.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.UserModel]:
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.UserModel]:
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def update_user(db: Session, user: schemas, username: str):
    db_user = get_user_by_username(db, username)
    user_data = user.dict()

    if user_data["password"]:
        password = get_hashed_password(user_data["password"])
        setattr(db_user, "password", password)

    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models]:
    user = get_user_by_username(db, username)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user
