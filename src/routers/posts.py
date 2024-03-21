
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from starlette import status

from src.schemas.post import *
from src.services.depends import get_db, get_current_active_user
from src.services.posts import get_post_by_title, get_post_by_id, get_post_by_slug

router = APIRouter(
    tags=[
        "posts"
    ]
)


@router.post("/", )
def create_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user= Depends(get_current_active_user)
) -> Response:
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=create_post(db, post)
    )


@router.get("/",response_model=PostInDB)
def get_all_posts(db = Depends()):
    return Response(
        status_code=status.HTTP_200_OK,
        content=get_all_posts(db)
    )


@router.get("/{post_id}", response_model=PostInDB)
def get_post(
        title: Optional[str] = None,
        post_id: Optional[int] = None,
        slug: Optional[str] = None,
        db: Session = Depends(get_db)
):
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

    return Response(
        status_code=status.HTTP_200_OK,
        content=db_post.dict()
    )


@router.put('/{post_id}')
def update_post(post_id: int, post):
    ...


@router.delete('/{post_id}', )
def delete_post(post_id):
    ...


