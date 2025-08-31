# 权限模块（Auth Module）说明

本模块提供用户认证与账户相关功能，采用低侵入、可选启用、独立存储的架构，便于在不影响主业务的情况下进行演进与扩展。本文档用于为后续添加新功能、修改和修复提供上下文。

## 设计原则与低侵入机制
- 低侵入：
  - 与主业务数据库、模型解耦：使用独立的 SQLAlchemy Base（`BaseAuth`）与独立连接，保持领域边界清晰。
  - 与主应用路由低耦合：仅在环境变量开启时挂载路由；不改动主路由设计。
- 可选启用：
  - 通过环境变量 `AUTH_MODULE_ENABLED=1` 激活，关闭时不会引入任何额外依赖与路由。
- 渐进式/幂等演进：
  - 在 SQLite 环境下，使用 `ensure_auth_schema()` 按需、幂等地为 users 表增加可选列，避免迁移对存量数据造成影响。

## 为什么采用独立数据库
- 隔离与安全：认证数据（密码哈希、重置令牌、邮箱验证令牌等）与主业务数据隔离，降低越权风险与误删风险。
- 运维与扩展：便于独立备份/恢复、独立迁移、独立伸缩（未来替换为更合适的存储/服务）。
- 规避耦合：权限域与内容域（主库）演进步调不同，独立可减少跨域修改的连锁影响。
- 本地开发友好：默认 `sqlite:///./auth_module.db` 即可使用，也可通过 `AUTH_DATABASE_URL` 切换到其他数据库。

## 目录结构概览
- `database_auth.py`：独立数据库引擎/会话、`BaseAuth`、`ensure_auth_schema`。
- `models_auth.py`：User、Favorite 等权限域模型。
- `schemas_auth.py`：Pydantic 模式（注册/登录/Token/收藏等）。
- `crud_auth.py`：用户与收藏的 CRUD 操作。
- `security.py`：密码哈希（bcrypt）、JWT 生成/校验（access/refresh）。
- `routes_auth.py`：FastAPI 路由与依赖注入（仅在开启模块时挂载）。

## 与主应用的集成
- 在 `app/main.py` 中按环境变量条件挂载：
  - `if AUTH_MODULE_ENABLED in ("1","true","True","yes","on"):` 则 `include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])`。
- 与主库的交互仅限 `/favorites/with-content` 接口：按收藏内容 ID 批量查询主库 Content 并返回摘要。

## 数据模型摘要
- User
  - 基本字段：`id, username, email, password_hash, created_at, updated_at`
  - Profile：`nickname, avatar_url, bio`
  - 邮箱验证：`email_verified, email_verify_token, email_verify_expire`
  - 密码重置：`reset_token, reset_token_expire`
- Favorite
  - `id, user_id, content_id, note, created_at`
  - 约束：`UniqueConstraint(user_id, content_id)` 防止重复收藏

## API 一览（共 11 项）
- 认证
  - POST `/api/v1/auth/register` 注册
  - POST `/api/v1/auth/login` 登录（OAuth2PasswordRequestForm）
  - POST `/api/v1/auth/refresh` 刷新令牌
  - GET  `/api/v1/auth/me` 当前用户信息
- 个人资料
  - GET  `/api/v1/auth/profile` 获取资料
  - PUT  `/api/v1/auth/profile` 更新资料
- 密码重置
  - POST `/api/v1/auth/password/reset/request` 申请重置（打印模拟邮件）
  - POST `/api/v1/auth/password/reset/confirm` 确认重置
- 邮箱验证
  - POST `/api/v1/auth/email/verify/request` 申请验证（打印模拟邮件）
  - POST `/api/v1/auth/email/verify/confirm` 确认验证
- 收藏
  - POST `/api/v1/auth/favorites` 新增收藏
  - GET  `/api/v1/auth/favorites` 列出收藏
  - GET  `/api/v1/auth/favorites/with-content` 附内容摘要的收藏列表
  - DELETE `/api/v1/auth/favorites/{content_id}` 取消收藏

> 说明：上述接口在代码中已实现，`with-content` 会从主库按 ID 批量拉取内容摘要并安全处理缺失项。

## 配置项
- `AUTH_MODULE_ENABLED`：是否启用权限模块（默认 0 关闭）。
- `AUTH_DATABASE_URL`：权限库连接串，默认 `sqlite:///./auth_module.db`。
- `AUTH_JWT_SECRET`：JWT 秘钥（默认开发值，生产必须覆盖）。
- `AUTH_ACCESS_TOKEN_MINUTES`：访问令牌有效期（默认 60 分钟）。
- `AUTH_REFRESH_TOKEN_DAYS`：刷新令牌有效期（默认 7 天）。

## 安全与可靠性要点（修复与改进日志）
- 幂等 schema 扩展（SQLite）：`ensure_auth_schema` 在 SQLite 下按需 `ALTER TABLE`，避免升级时失败或重复变更。
- Token 类型校验：`/me`、`/refresh` 等统一校验 JWT `type` 字段，防止用 refresh 充当 access（或反之）。
- 防用户枚举：密码重置与邮箱验证的申请接口对不存在的邮箱返回统一响应，避免旁路探测用户资产。
- 收藏唯一性：`favorites` 上增加 `(user_id, content_id)` 唯一约束，杜绝重复收藏造成的数据异常。
- 缺失内容容错：`/favorites/with-content` 对主库中已删除/缺失的内容返回 `content=None`，避免 500。
- 密码存储：采用 `passlib[bcrypt]` 存储密码哈希；禁止明文口令。
- 过期与配置化：`access/refresh` 过期时间可配置，默认分别为 60 分钟与 7 天。

> 以上项为当前代码中已落地的安全与鲁棒性措施，作为问题修复与设计优化的基线。

## 扩展与二次开发建议
- 增加用户属性：
  - SQLite 环境下，通过在 `ensure_auth_schema` 中追加列定义；其他数据库请使用标准迁移工具（如 Alembic）。
- 新增接口：
  - 在 `routes_auth.py` 中添加路由，必要时在 `schemas_auth.py` 增加请求/响应模型，业务写在 `crud_auth.py`。
- 与主库的弱耦合交互：
  - 仅通过 ID 协议与主库交互，避免跨库外键；必要时在路由层做聚合返回。

## 注意事项
- 生产环境请务必配置强随机的 `AUTH_JWT_SECRET`。
- 若切换到非 SQLite 数据库，请用迁移工具管理 schema 变更（`ensure_auth_schema` 仅在 SQLite 下生效）。
- 关闭模块（`AUTH_MODULE_ENABLED=0`）后，所有 `/api/v1/auth` 路由均不会加载。