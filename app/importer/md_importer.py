import os
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session

from app import crud
from app.models import Content as ContentModel
from .md_parser import parse_markdown


def import_markdown_file(db: Session, file_path: str, overwrite: bool = False) -> Tuple[str, ContentModel | None]:
    """Import a single .md file into DB. Returns (status, content_obj) where status is one of
    'created', 'updated', 'skipped', 'failed'."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        base_dir = os.path.dirname(os.path.abspath(file_path))
        _meta, payload = parse_markdown(text, base_dir=base_dir)
        title = payload.get('title')
        if not title:
            return ("failed", None)

        existing = crud.get_content_by_title(db, title)
        if existing:
            if overwrite:
                # update in-place
                existing.module = payload.get('module', existing.module)
                existing.subcategory = payload.get('subcategory', existing.subcategory)
                existing.content_body = payload.get('content_body', existing.content_body)
                existing.python_code = payload.get('python_code', existing.python_code)
                existing.formulas = payload.get('formulas', existing.formulas)
                existing.charts_data = payload.get('charts_data', existing.charts_data)
                existing.tags = payload.get('tags', existing.tags)
                db.add(existing)
                db.commit()
                db.refresh(existing)
                return ("updated", existing)
            else:
                return ("skipped", existing)
        else:
            obj = crud.create_content(db, payload)
            return ("created", obj)
    except Exception:
        return ("failed", None)


def import_directory(db: Session, dir_path: str, overwrite: bool = False) -> List[Dict[str, Any]]:
    """Import all .md files under a directory (non-recursive)."""
    results: List[Dict[str, Any]] = []
    for name in os.listdir(dir_path):
        if not name.lower().endswith('.md'):
            continue
        p = os.path.join(dir_path, name)
        status, obj = import_markdown_file(db, p, overwrite=overwrite)
        results.append({
            'file': name,
            'status': status,
            'id': getattr(obj, 'id', None),
            'title': getattr(obj, 'title', None),
        })
    return results

# New: import from raw markdown text (for API)

def import_markdown_text(db: Session, md_text: str, *, base_dir: str | None = None, overwrite: bool = False) -> Tuple[str, ContentModel | None]:
    """
    Import a Markdown text into DB. Returns (status, content_obj).
    """
    try:
        _meta, payload = parse_markdown(md_text, base_dir=base_dir)
        title = payload.get('title')
        if not title:
            return ("failed", None)
        existing = crud.get_content_by_title(db, title)
        if existing:
            if overwrite:
                existing.module = payload.get('module', existing.module)
                existing.subcategory = payload.get('subcategory', existing.subcategory)
                existing.content_body = payload.get('content_body', existing.content_body)
                existing.python_code = payload.get('python_code', existing.python_code)
                existing.formulas = payload.get('formulas', existing.formulas)
                existing.charts_data = payload.get('charts_data', existing.charts_data)
                existing.tags = payload.get('tags', existing.tags)
                db.add(existing)
                db.commit()
                db.refresh(existing)
                return ("updated", existing)
            else:
                return ("skipped", existing)
        else:
            obj = crud.create_content(db, payload)
            return ("created", obj)
    except Exception:
        return ("failed", None)