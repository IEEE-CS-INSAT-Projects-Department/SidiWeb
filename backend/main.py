from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.register import router as register_router
from routers.login import router as login_router
from routers.me import router as me_router
from routers.media import router as media_router
from routers.recommendations import router as recommendations_router
from src.sites.routers.sites import router as sites_router
from src.sites.routers.templates import router as templates_router

from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from datetime import datetime,timezone, timedelta
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting SidiWeb Auth API in {settings.environment} environment")
    
    # Initialize application state
    app.state.startup_time = datetime.now(timezone.utc)
    # app.state.version = "0.1.0"
    app.state.environment = settings.environment
    
    try:
        # Database connection is lazy, but we can ping to verify
        from database.connection import ping_db
        if await ping_db():
            logger.info("Database connection verified")
        else:
            logger.warning("Database connection check failed")

        # Seed the template catalogue (read-only) once at startup
        try:
            from database.connection import get_db
            from src.sites.crud import seed_templates
            await seed_templates(get_db())
            logger.info("Templates seeded")
        except Exception as e:
            logger.warning(f"Template seeding skipped: {e}")

        yield
        
    finally:
        # Shutdown
        logger.info("Shutting down SidiWeb Auth API")
        
        try:
            from database.connection import close_db
            await close_db()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f" Error closing database: {e}")
        
        logger.info("Shutdown complete")


def create_application() -> FastAPI:
    app = FastAPI(
        title="SidiWeb Backend - Auth Module",
        description="Authentication & User Management API",
        version="0.1.0",
        lifespan=lifespan,  
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        openapi_url="/openapi.json" if settings.environment != "production" else None,
    )
    
    # Configure CORS
    configure_cors(app)
    
    # Register routers
    register_routers(app)
    
    return app


def configure_cors(app: FastAPI) -> None:
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    headers = ["Authorization", "Content-Type"]

    if settings.environment == "production":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://SidiWeb.com", "https://www.SidiWeb.com"],
            allow_credentials=True,
            allow_methods=methods,
            allow_headers=headers,
        )
    else:
        # Development: accept localhost / 127.0.0.1 / [::1] on any port
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?",
            allow_credentials=True,
            allow_methods=methods,
            allow_headers=headers,
        )


def register_routers(app: FastAPI) -> None:
    app.include_router(register_router)
    app.include_router(login_router)
    app.include_router(me_router)
    app.include_router(media_router)
    app.include_router(recommendations_router)
    app.include_router(sites_router)
    app.include_router(templates_router)



# Create application
app = create_application()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {
        "message": "Welcome to SidiWeb Authentication API",
        "version": app.state.version if hasattr(app.state, 'version') else "0.1.0",
        "environment": app.state.environment if hasattr(app.state, 'environment') else settings.environment,
        "status": "running",
        "docs": "/docs" if settings.environment != "production" else None,
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    from database.connection import ping_db
    
    try:
        db_healthy = await ping_db()
        
        return {
            "status": "healthy" if db_healthy else "degraded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": "connected" if db_healthy else "disconnected",
            "uptime": str(datetime.now(timezone.utc) - app.state.startup_time) if hasattr(app.state, 'startup_time') else "unknown",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": exc.body,
            "path": request.url.path
        })
    )