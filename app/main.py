from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.config import APP_NAME, APP_VERSION


# ==========================================================
# Startup & Shutdown Lifecycle
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("=" * 60)
    print("🚀 Starting Intelligent Email Automation API")
    print("=" * 60)

    # Preload heavy models here (recommended)
    # Example:
    # load_spam_model()
    # load_embedding_model()
    # init_chroma_db()

    yield

    print("=" * 60)
    print("🛑 Stopping Intelligent Email Automation API")
    print("=" * 60)


# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI Powered Email Automation using ML + RAG + LLM",
    lifespan=lifespan
)


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


# ==========================================================
# Static Files (SAFE CHECK)
# ==========================================================

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )


# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ==========================================================
# API Routes
# ==========================================================

app.include_router(router)


# ==========================================================
# FRONTEND ROUTE
# ==========================================================

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {"title": APP_NAME}
    )


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
async def health():

    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "application": APP_NAME,
            "version": APP_VERSION
        }
    )


# ==========================================================
# API INFO
# ==========================================================

@app.get("/api")
async def api_information():

    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "documentation": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.exception_handler(404)
async def not_found(request: Request, exc):

    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Page Not Found"
        }
    )


@app.exception_handler(500)
async def server_error(request: Request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error"
        }
    )


# ==========================================================
# MAIN RUNNER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )