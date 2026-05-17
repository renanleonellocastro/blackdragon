import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings

logger = logging.getLogger("blackdragon")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        logger.info("%s %s %s %.1fms", request.method, request.url.path, response.status_code, elapsed)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="BlackDragon API",
        description="Smart Home Automation Platform API",
        version="0.1.0",
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    from app.api.admin import router as admin_router
    from app.api.auth import router as auth_router
    from app.api.blog import router as blog_router
    from app.api.boards import router as boards_router
    from app.api.compiler import router as compiler_router
    from app.api.deployments import router as deployments_router
    from app.api.diagrams import router as diagrams_router
    from app.api.leads import router as leads_router
    from app.api.modules import router as modules_router
    from app.api.projects import router as projects_router
    from app.api.properties import router as properties_router

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
    app.include_router(blog_router, prefix="/api/blog", tags=["blog"])
    app.include_router(properties_router, prefix="/api/properties", tags=["properties"])
    app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
    app.include_router(diagrams_router, prefix="/api/projects", tags=["diagrams"])
    app.include_router(deployments_router, prefix="/api/projects", tags=["deployments"])
    app.include_router(boards_router, prefix="/api/boards", tags=["boards"])
    app.include_router(compiler_router, prefix="/api/compiler", tags=["compiler"])
    app.include_router(modules_router, prefix="/api/modules", tags=["modules"])
    app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

    @app.get("/api/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
