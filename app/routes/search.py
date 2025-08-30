from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/search/", response_model=schemas.SearchResults)
def search_content(
    query: str = Query(..., description="搜索关键词"),
    module: Optional[str] = Query(None, description="模块过滤"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    search_conditions = [
        models.Content.title.ilike(f"%{query}%"),
        models.Content.content_body.ilike(f"%{query}%"),
        models.Content.python_code.ilike(f"%{query}%"),
    ]

    if module:
        query_obj = db.query(models.Content).filter(
            models.Content.module == module,
            or_(*search_conditions),
        )
    else:
        query_obj = db.query(models.Content).filter(or_(*search_conditions))

    total_count = query_obj.count()
    results = query_obj.offset(skip).limit(limit).all()

    return schemas.SearchResults(results=results, total_count=total_count)