
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        minute_ago = now - 60
        self.requests[client_ip] = [t for t in self.requests[client_ip] if t > minute_ago]
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.requests[client_ip].append(now)
        response = await call_next(request)
        return response


class AuditMiddleware(BaseHTTPMiddleware):
    SENSITIVE_PATHS = ["/api/v1/auth/login", "/api/v1/auth/register"]

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        if request.url.path in self.SENSITIVE_PATHS:
            logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
        response.headers["X-Request-Duration"] = f"{duration:.3f}"
        return response


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://app.ai-crm.io"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
