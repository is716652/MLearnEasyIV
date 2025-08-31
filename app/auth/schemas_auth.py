from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    email_verified: Optional[bool] = False

    class Config:
        orm_mode = True


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class FavoriteCreate(BaseModel):
    content_id: int
    note: Optional[str] = None


class FavoriteOut(BaseModel):
    id: int
    content_id: int
    note: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerifyRequest(BaseModel):
    email: EmailStr


class EmailVerifyConfirm(BaseModel):
    token: str


# 新增：用于 /favorites/with-content 响应
class ContentSummary(BaseModel):
    id: int
    title: str
    module: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class FavoriteWithContent(BaseModel):
    id: int
    content_id: int
    note: Optional[str] = None
    created_at: datetime
    content: Optional[ContentSummary] = None

    class Config:
        orm_mode = True