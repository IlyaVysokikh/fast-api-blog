from typing import Optional

from sqlalchemy.orm import Session

from src import models, schemas
from src.models.post import PostModel


def get_post_by_title(title: str, db: Session):
    return db.query(models.PostModel).filter(title=title).first()


def get_post_by_slug(slug: str, db: Session):
    return db.query(models.PostModel).filter(slug=slug).first()


def get_post_by_id(post_id: int, db: Session):
    ...


def get_post_by_author(author_id: int, db: Session):
    ...


def create_post():
    ...


def update_post():
    ...


def delete_post():
    ...


def get_all_posts(db: Session):
    ...
