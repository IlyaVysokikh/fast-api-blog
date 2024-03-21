from typing import Any

from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    username: str
    email: str
    bio: str
    is_active: bool


class UserCreate(UserBase):
    password: str

    @validator("username")
    def validate_username(cls: Any, username: str) -> str:
        if len(username) < 3:
            raise ValueError("username cannot be shorter than 3 characters")
        return username

    @validator("email")
    def validate_email(cls: Any, email: str) -> str:
        if len(email) == 0:
            raise ValueError("An email is required")
        return email


class User(UserBase):
    id: int = None

    class Config:
        orm_mode: bool = True


class UserInDB(User):
    hashed_password: str


class Users(User):
    id: int


class UserUpdate(UserBase):
    password: str

    class Config:
        orm_mode: bool = True
