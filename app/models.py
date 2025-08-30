from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.types import JSON
from datetime import datetime

from .database import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(50), index=True)
    subcategory = Column(String(100), index=True)
    title = Column(String(200), index=True, unique=True)
    content_body = Column(Text)
    python_code = Column(Text)
    formulas = Column(JSON)
    charts_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON)


class ContentUpdateLog(Base):
    __tablename__ = "content_update_log"

    id = Column(Integer, primary_key=True)
    update_type = Column(String(50))
    content_count = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)