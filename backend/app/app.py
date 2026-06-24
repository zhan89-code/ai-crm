
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.database import init_db, engine
from app.api.v1.router import api_router
from app.core.security import setup_cors, RateLimitMiddleware, AuditMiddleware
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up AI CRM API...")
    await init_db()
    yield
    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="AI CRM API",
    description="AI-Powered CRM for SMBs",
    version="0.1.0",
    lifespan=lifespan,
)

setup_cors(app)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(AuditMiddleware)

app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://api.ai-crm.io/errors/internal",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred",
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
