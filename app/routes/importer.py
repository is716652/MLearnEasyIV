from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.importer.md_importer import import_markdown_text

router = APIRouter()


@router.post("/import-md/text")
def import_md_from_text(req: schemas.ImportMdTextRequest, db: Session = Depends(get_db)):
    status, obj = import_markdown_text(db, req.md_text, base_dir=req.base_dir, overwrite=req.overwrite)
    return {"status": status, "id": getattr(obj, "id", None), "title": getattr(obj, "title", None)}


@router.post("/import-md/file")
async def import_md_from_file(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    overwrite: bool = Form(False),
    base_dir: Optional[str] = Form(None),
):
    data = await file.read()
    text = data.decode("utf-8", errors="ignore")
    status, obj = import_markdown_text(db, text, base_dir=base_dir, overwrite=overwrite)
    return {"status": status, "id": getattr(obj, "id", None), "title": getattr(obj, "title", None)}


@router.post("/import-md/files")
async def import_md_from_files(
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...),
    overwrite: bool = Form(False),
    base_dir: Optional[str] = Form(None),
):
    results: List[dict] = []
    for f in files:
        data = await f.read()
        text = data.decode("utf-8", errors="ignore")
        status, obj = import_markdown_text(db, text, base_dir=base_dir, overwrite=overwrite)
        results.append({
            "file": f.filename,
            "status": status,
            "id": getattr(obj, "id", None),
            "title": getattr(obj, "title", None),
        })
    return {"results": results}