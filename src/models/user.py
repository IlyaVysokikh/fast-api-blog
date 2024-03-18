from sqlalchemy import Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean

from src.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__: str = 'users'

    username: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(50), unique=True, nullable=False)
    hashed_password: str = Column(String(), nullable=False)
    bio: str = Column(Text, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=False)