from typing import Optional, List
from sqlalchemy.orm import Session
from .security import hash_password, verify_password
from . import models_auth


# Users

def get_user_by_username(db: Session, username: str) -> Optional[models_auth.User]:
    return db.query(models_auth.User).filter(models_auth.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models_auth.User]:
    return db.query(models_auth.User).filter(models_auth.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models_auth.User]:
    return db.query(models_auth.User).get(user_id)


def create_user(db: Session, username: str, email: str, password: str) -> models_auth.User:
    user = models_auth.User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models_auth.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def update_profile(db: Session, user: models_auth.User, nickname: Optional[str], avatar_url: Optional[str], bio: Optional[str]) -> models_auth.User:
    if nickname is not None:
        user.nickname = nickname
    if avatar_url is not None:
        user.avatar_url = avatar_url
    if bio is not None:
        user.bio = bio
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def set_reset_token(db: Session, user: models_auth.User, token: str, expire_at) -> models_auth.User:
    user.reset_token = token
    user.reset_token_expire = expire_at
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def clear_reset_token_and_set_password(db: Session, user: models_auth.User, new_password: str) -> models_auth.User:
    user.password_hash = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expire = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def set_email_verify_token(db: Session, user: models_auth.User, token: str, expire_at) -> models_auth.User:
    user.email_verify_token = token
    user.email_verify_expire = expire_at
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def confirm_email_verified(db: Session, user: models_auth.User) -> models_auth.User:
    user.email_verified = True
    user.email_verify_token = None
    user.email_verify_expire = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Favorites

def add_favorite(db: Session, user_id: int, content_id: int, note: Optional[str] = None) -> models_auth.Favorite:
    fav = models_auth.Favorite(user_id=user_id, content_id=content_id, note=note)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


def list_favorites(db: Session, user_id: int) -> List[models_auth.Favorite]:
    return db.query(models_auth.Favorite).filter(models_auth.Favorite.user_id == user_id).all()


def remove_favorite(db: Session, user_id: int, content_id: int) -> int:
    q = db.query(models_auth.Favorite).filter(
        models_auth.Favorite.user_id == user_id,
        models_auth.Favorite.content_id == content_id,
    )
    count = q.count()
    if count:
        q.delete()
        db.commit()
    return count