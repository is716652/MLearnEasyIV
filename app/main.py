from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import os

from app.database import engine, Base
from app.routes import content, search, utils, importer

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="简单学机器学习API",
    description="为「简单学机器学习」APP提供的后端API",
    version="1.0.0",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static
os.makedirs("app/static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(utils.router, prefix="/api/v1", tags=["utils"])
app.include_router(importer.router, prefix="/api/v1", tags=["importer"])

# Conditionally include auth module
if os.getenv("AUTH_MODULE_ENABLED", "0") in ("1", "true", "True", "yes", "on"):
    from app.auth import routes_auth as auth_routes
    app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"]) 


# Re-enable Swagger UI at /docs
@app.get("/docs")
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Swagger UI")


@app.get("/")
async def root():
    return {"message": "欢迎使用简单学机器学习API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}