from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from .database_auth import get_db_auth, BaseAuth, engine_auth, ensure_auth_schema
from . import crud_auth, schemas_auth, models_auth
from .security import create_access_token, create_refresh_token, decode_token

# 新增导入
from datetime import datetime, timedelta
import secrets
from app.database import get_db
from app import models as main_models

# 确保权限库表创建并做低侵入扩展
BaseAuth.metadata.create_all(bind=engine_auth)
ensure_auth_schema()

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=schemas_auth.UserOut)
def register(user: schemas_auth.UserCreate, db: Session = Depends(get_db_auth)):
    if crud_auth.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if crud_auth.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已存在")
    created = crud_auth.create_user(db, user.username, user.email, user.password)
    return created


@router.post("/login", response_model=schemas_auth.TokenPair)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_auth)):
    user = crud_auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh", response_model=schemas_auth.TokenPair)
def refresh(req: schemas_auth.RefreshRequest, db: Session = Depends(get_db_auth)):
    payload = decode_token(req.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="无效或过期的刷新令牌")
    user_id = int(payload.get("sub", 0))
    user = db.query(models_auth.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    access = create_access_token(subject=str(user.id))
    # 简单实现：同步返回新的 refresh，未做轮换黑名单
    refresh = create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.get("/me", response_model=schemas_auth.UserOut)
def me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    user = db.query(models_auth.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


# Profile
@router.get("/profile", response_model=schemas_auth.UserOut)
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    user = db.query(models_auth.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/profile", response_model=schemas_auth.UserOut)
def update_profile(req: schemas_auth.ProfileUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    user = db.query(models_auth.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    updated = crud_auth.update_profile(db, user, req.nickname, req.avatar_url, req.bio)
    return updated


# Password Reset
@router.post("/password/reset/request")
def password_reset_request(req: schemas_auth.PasswordResetRequest, db: Session = Depends(get_db_auth)):
    user = crud_auth.get_user_by_email(db, req.email)
    if not user:
        # 为防止枚举用户，返回统一响应
        return {"status": "ok"}
    token = secrets.token_urlsafe(32)
    expire_at = datetime.utcnow() + timedelta(hours=1)
    crud_auth.set_reset_token(db, user, token, expire_at)
    # 模拟发送邮件：打印到日志
    print(f"[Password Reset] 点击链接重置密码: /api/v1/auth/password/reset/confirm?token={token}")
    return {"status": "ok"}


@router.post("/password/reset/confirm")
def password_reset_confirm(req: schemas_auth.PasswordResetConfirm, db: Session = Depends(get_db_auth)):
    user = db.query(models_auth.User).filter(models_auth.User.reset_token == req.token).first()
    if not user or not user.reset_token_expire or user.reset_token_expire < datetime.utcnow():
        raise HTTPException(status_code=400, detail="无效或过期的重置令牌")
    crud_auth.clear_reset_token_and_set_password(db, user, req.new_password)
    return {"status": "ok"}


# Email Verification
@router.post("/email/verify/request")
def email_verify_request(req: schemas_auth.EmailVerifyRequest, db: Session = Depends(get_db_auth)):
    user = crud_auth.get_user_by_email(db, req.email)
    if not user:
        return {"status": "ok"}
    token = secrets.token_urlsafe(32)
    expire_at = datetime.utcnow() + timedelta(hours=24)
    crud_auth.set_email_verify_token(db, user, token, expire_at)
    print(f"[Email Verify] 点击链接完成验证: /api/v1/auth/email/verify/confirm?token={token}")
    return {"status": "ok"}


@router.post("/email/verify/confirm")
def email_verify_confirm(req: schemas_auth.EmailVerifyConfirm, db: Session = Depends(get_db_auth)):
    user = db.query(models_auth.User).filter(models_auth.User.email_verify_token == req.token).first()
    if not user or not user.email_verify_expire or user.email_verify_expire < datetime.utcnow():
        raise HTTPException(status_code=400, detail="无效或过期的验证令牌")
    crud_auth.confirm_email_verified(db, user)
    return {"status": "ok"}


@router.post("/favorites", response_model=schemas_auth.FavoriteOut)
def add_favorite(req: schemas_auth.FavoriteCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    fav = crud_auth.add_favorite(db, user_id=user_id, content_id=req.content_id, note=req.note)
    return fav


@router.get("/favorites", response_model=List[schemas_auth.FavoriteOut])
def list_favorites(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    return crud_auth.list_favorites(db, user_id=user_id)


@router.get("/favorites/with-content", response_model=List[schemas_auth.FavoriteWithContent])
def list_favorites_with_content(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth), main_db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    favs = crud_auth.list_favorites(db, user_id=user_id)
    content_ids = [f.content_id for f in favs]
    contents = []
    if content_ids:
        contents = main_db.query(main_models.Content).filter(main_models.Content.id.in_(content_ids)).all()
    content_map = {c.id: c for c in contents}
    result: List[schemas_auth.FavoriteWithContent] = []
    for f in favs:
        c = content_map.get(f.content_id)
        summary = None
        if c:
            summary = schemas_auth.ContentSummary(
                id=c.id,
                title=c.title,
                module=c.module,
                subcategory=c.subcategory,
                tags=c.tags,
                created_at=c.created_at,
            )
        result.append(schemas_auth.FavoriteWithContent(
            id=f.id,
            content_id=f.content_id,
            note=f.note,
            created_at=f.created_at,
            content=summary,
        ))
    return result


@router.delete("/favorites/{content_id}")
def remove_favorite(content_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_auth)):
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    user_id = int(payload.get("sub", 0))
    deleted = crud_auth.remove_favorite(db, user_id=user_id, content_id=content_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="未找到收藏记录")
    return {"deleted": deleted}