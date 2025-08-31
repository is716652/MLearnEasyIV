from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 独立权限库，默认sqlite文件 auth_module.db（可通过环境变量 AUTH_DATABASE_URL 覆盖）
AUTH_DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite:///./auth_module.db")

engine_auth = create_engine(
    AUTH_DATABASE_URL,
    connect_args={"check_same_thread": False} if AUTH_DATABASE_URL.startswith("sqlite") else {},
    echo=True,
)

SessionLocalAuth = sessionmaker(autocommit=False, autoflush=False, bind=engine_auth)

BaseAuth = declarative_base()


def get_db_auth():
    db = SessionLocalAuth()
    try:
        yield db
    finally:
        db.close()


def ensure_auth_schema():
    """在 SQLite 下以低侵入方式为 users 表添加新列，用于后续扩展。"""
    if not AUTH_DATABASE_URL.startswith("sqlite"):
        return
    with engine_auth.connect() as conn:
        # users 表新增列
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(users)"))}
        def add_col_if_missing(col_name: str, col_def: str):
            if col_name not in cols:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_def}"))
        add_col_if_missing("nickname", "nickname TEXT")
        add_col_if_missing("avatar_url", "avatar_url TEXT")
        add_col_if_missing("bio", "bio TEXT")
        add_col_if_missing("email_verified", "email_verified BOOLEAN DEFAULT 0")
        add_col_if_missing("email_verify_token", "email_verify_token TEXT")
        add_col_if_missing("email_verify_expire", "email_verify_expire DATETIME")
        add_col_if_missing("reset_token", "reset_token TEXT")
        add_col_if_missing("reset_token_expire", "reset_token_expire DATETIME")
        conn.commit()