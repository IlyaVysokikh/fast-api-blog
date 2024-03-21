from sqlalchemy.orm import Session

from src import models, schemas
from slugify import slugify
from sqlalchemy import desc


def get_post_by_title(title: str, db: Session):
    return db.query(models.PostModel).filter(title=title).first()


def get_post_by_slug(slug: str, db: Session):
    return db.query(models.PostModel).filter(slug=slug).first()


def get_post_by_id(post_id: int, db: Session):
    return db.query(models.PostModel).filter(id=id).first()


def get_post_by_author(author_id: int, db: Session):
    return db.query(models.PostModel).filter(author_id=author_id).first()


def create_post(db: Session, post, current_user):
    post_data = post.dict()
    post_data['slug'] = slugify(post_data['title'])
    user_data = schemas.user.User.from_orm(current_user).dict()
    post_data['author_id'] = user_data['id']
    db_post = models.post.PostModel(**post_data)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def update_post(db: Session, post: str, slug: str):
    db_post = get_post_by_slug(slug, db)
    post_data: dict = post.dict()
    setattr(db_post, "title", post_data["title"])
    setattr(db_post, "slug", slugify(post_data["title"]))
    setattr(db_post, "body", post_data["body"])

    db.commit()
    db.refresh(db_post)

    return db_post


def delete_post(db: Session, slug: str):
    db_post = get_post_by_slug(slug, db)
    db.delete(db_post)
    db.commit()
    return None


def get_all_posts(db: Session):
    return db.query(models.post.PostModel).order_by(desc(models.post.PostModel.created_at))


def count_post(db: Session) -> int:
    return db.query(models.post.PostModel).count()