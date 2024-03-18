from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, StrictBool, field_validator


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):

    @field_validator("title")
    def validate_title(cls: Any, title: str, **kwargs: Any) -> str:
        if len(title) == 0:
            raise ValueError("Title cannot be empty")
        elif len(title) > 100:
            raise ValueError("Title is too long")
        return title

    @field_validator("body")
    def validate_body(cls: Any, body: str, **kwargs: Any) -> str:
        if len(body) == 0:
            raise ValueError("Body cannot be empty")
        return body
