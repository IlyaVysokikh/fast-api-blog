from datetime import datetime

from sqlalchemy import Integer, TIMESTAMP
from sqlalchemy.sql.schema import Column
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)

    created_at: Mapped[datetime] = Column(
        TIMESTAMP(timezone=True),
        default=datetime.now()
    )
    updated_at: Mapped[datetime] = Column(
        TIMESTAMP(timezone=True),
        default=datetime.now(),
        onupdate=datetime.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"