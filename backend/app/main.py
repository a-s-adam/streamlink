from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .api.routes import router as api_router


def create_app() -> FastAPI:
    """Create the FastAPI application and register routers and middleware."""
    settings: Settings = get_settings()
    app = FastAPI(
        title="Personal Entertainment Knowledge Graph API",
        description="API backend for the PEKG MVP. Handles ingestion, metadata enrichment, and recommendations.",
        version="0.1.0",
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
        return {"message": "Welcome to the Personal Entertainment Knowledge Graph API"}

    # Health check
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    # Register routers
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
