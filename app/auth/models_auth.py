from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, UniqueConstraint, Boolean
from .database_auth import BaseAuth


class User(BaseAuth):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # Profile fields
    nickname = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    # Email verification
    email_verified = Column(Boolean, default=False)
    email_verify_token = Column(String(255), nullable=True)
    email_verify_expire = Column(DateTime, nullable=True)
    # Password reset
    reset_token = Column(String(255), nullable=True)
    reset_token_expire = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Favorite(BaseAuth):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    # 关联主库 content.id（不做外键约束，低耦合）
    content_id = Column(Integer, index=True, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='uq_user_content'),
    )