from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas, crud
from app.ml_content.content_generator import ContentGenerator
from app.init_database import populate_math_contents, populate_ml_contents

router = APIRouter()
content_generator = ContentGenerator()


@router.get("/content/", response_model=List[schemas.Content])
def read_content(
    module: Optional[str] = Query(None, description="模块: math/ml/dl"),
    subcategory: Optional[str] = Query(None, description="子分类"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_content(db, module=module, subcategory=subcategory, skip=skip, limit=limit)


@router.get("/content/{content_id}", response_model=schemas.Content)
def read_content_by_id(content_id: int, db: Session = Depends(get_db)):
    content = crud.get_content_by_id(db, content_id=content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="内容未找到")
    return content


@router.post("/content/generate/", response_model=schemas.Content)
def generate_content(request: schemas.GenerateRequest, db: Session = Depends(get_db)):
    existing_content = crud.get_content_by_title(db, request.title)
    if existing_content:
        return existing_content

    generated_data = content_generator.generate_content(
        request.module, request.subcategory, request.title
    )

    content_data = {
        "module": request.module,
        "subcategory": request.subcategory,
        "title": request.title,
        **generated_data,
    }

    return crud.create_content(db, content_data)


@router.post("/content/init_math")
def init_math_content(db: Session = Depends(get_db)):
    """批量初始化数学内容，返回新增记录数"""
    created = populate_math_contents(db, content_generator)
    return {"status": "ok", "created": created}


@router.post("/content/init_ml")
def init_ml_content(db: Session = Depends(get_db)):
    """批量初始化机器学习内容，返回新增记录数"""
    created = populate_ml_contents(db, content_generator)
    return {"status": "ok", "created": created}


@router.post("/content/update/")
def update_content(request: schemas.ContentUpdateRequest, db: Session = Depends(get_db)):
    """根据模块/子类批量再生成内容，并更新现有记录（用于结构变更或内容刷新）。"""
    query = db.query(models.Content)
    # 仅筛选指定模块
    if request.modules:
        query = query.filter(models.Content.module.in_(request.modules))
    # 可选：筛选子分类
    if request.subcategories:
        query = query.filter(models.Content.subcategory.in_(request.subcategories))

    items: List[models.Content] = query.all()
    updated = 0

    for item in items:
        # 使用同一生成器按原有三元组(module, subcategory, title)再生成
        generated = content_generator.generate_content(item.module, item.subcategory, item.title)
        # 覆盖更新关键字段
        if "content_body" in generated:
            item.content_body = generated["content_body"]
        if "python_code" in generated:
            item.python_code = generated["python_code"]
        if "formulas" in generated:
            item.formulas = generated["formulas"]
        if "charts_data" in generated:
            item.charts_data = generated["charts_data"]
        if "tags" in generated:
            item.tags = generated["tags"]
        db.add(item)
        updated += 1

    if updated:
        db.commit()

    return {"status": "ok", "updated": updated}