from datetime import timedelta
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from starlette import status

from src import schemas
from src.services.depends import get_db
from src.services.posts import get_post_by_title, get_post_by_id, get_post_by_slug

router = APIRouter(
    tags=[
        "posts"
    ]
)


@router.post("/", response_model=schemas)
def create_post(post: schemas, db: Session = Depends(get_db)):
    ...


@router.get("/", response_model=schemas)
def get_all_posts(db: Session = Depends()):
    ...


@router.get("/{post_id}")
def get_post(title: Optional[str] = None, post_id: Optional[int] = None, slug: Optional[str] = None, db: Session = Depends(get_db)):
    if title:
        db_post = get_post_by_title(title, db)
    elif post_id:
        db_post = get_post_by_id(post_id, db)
    elif slug:
        db_post = get_post_by_slug(slug, db)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )

    return db_post

@router.put('/{post_id}', response_model=schemas)
def update_post(post_id: int, post: schemas):
    ...


@router.delete('/{post_id}', response_model=schemas)
def delete_post(post_id):
    ...


