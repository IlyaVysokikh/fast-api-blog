from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from src.models.user import UserModel
from src.models.base_model import BaseModel


class Post(BaseModel):
    __tablename__: str = 'posts'

    author_id: int = Column(Integer, primary_key=True)
    slug: str = Column(String, index=True)
    title: str = Column(String(100), index=True, nullable=False)
    body: str = Column(String(), index=False, nullable=False)
    published_at: datetime = Column(
        TIMESTAMP(timezone=True), default=datetime.now()
    )
    