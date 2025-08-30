from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ContentBase(BaseModel):
    module: str
    subcategory: str
    title: str
    content_body: str
    python_code: str
    formulas: Optional[Dict[str, Any]] = None
    charts_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class ContentCreate(ContentBase):
    pass


class Content(BaseModel):
    module: str
    subcategory: str
    title: str
    content_body: str
    python_code: str
    formulas: Optional[Dict[str, Any]] = None
    charts_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    query: str
    module: Optional[str] = None
    limit: int = 10
    offset: int = 0


class SearchResults(BaseModel):
    results: List[Content]
    total_count: int


class ContentUpdateRequest(BaseModel):
    modules: List[str]
    subcategories: Optional[List[str]] = None


class GenerateRequest(BaseModel):
    module: str
    subcategory: str
    title: str


class ImportMdTextRequest(BaseModel):
    md_text: str
    overwrite: bool = False
    base_dir: Optional[str] = None