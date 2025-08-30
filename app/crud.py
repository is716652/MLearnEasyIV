from sqlalchemy.orm import Session
from typing import List, Optional
from . import models


def get_content(db: Session, module: Optional[str] = None, subcategory: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.Content]:
    query = db.query(models.Content)
    if module:
        query = query.filter(models.Content.module == module)
    if subcategory:
        query = query.filter(models.Content.subcategory == subcategory)
    return query.offset(skip).limit(limit).all()


def get_content_by_id(db: Session, content_id: int) -> Optional[models.Content]:
    return db.query(models.Content).filter(models.Content.id == content_id).first()


def get_content_by_title(db: Session, title: str) -> Optional[models.Content]:
    return db.query(models.Content).filter(models.Content.title == title).first()


def create_content(db: Session, content_data: dict) -> models.Content:
    obj = models.Content(**content_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj