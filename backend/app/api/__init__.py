"""API package initialization."""

from fastapi import APIRouter

from .auth import router as auth_router
from .items import router as items_router
from .ingest import router as ingest_router
from .recommendations import router as recommendations_router
from .jobs import router as jobs_router

# Create main router
router = APIRouter()

# Include all routers
router.include_router(auth_router)
router.include_router(items_router)
router.include_router(ingest_router)
router.include_router(recommendations_router)
router.include_router(jobs_router)

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "streamlink-api"}
