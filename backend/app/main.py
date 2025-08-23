"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .api import router as api_router
from .db.database import create_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Streamlink API...")
    
    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Streamlink API...")


def create_app() -> FastAPI:
    """Create the FastAPI application and register routers and middleware."""
    settings: Settings = get_settings()
    
    app = FastAPI(
        title="Streamlink MVP API",
        description="API backend for the Streamlink MVP. Handles ingestion, metadata enrichment, and recommendations.",
        version="0.1.0",
        lifespan=lifespan
    )

    # Configure CORS
    origins = settings.cors_origins
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[origin.strip() for origin in origins.split(",")],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Root endpoint
    @app.get("/")
    async def read_root() -> dict[str, str]:
        return {
            "message": "Welcome to the Streamlink MVP API",
            "version": "0.1.0",
            "docs": "/docs"
        }

    # Health check
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok", "service": "streamlink-api"}

    # Register API router
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
