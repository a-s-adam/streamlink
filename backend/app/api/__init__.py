"""API package for the PEKG backend.

This module exposes a single ``router`` instance that aggregates all API routes
defined in submodules.  The router is included in the FastAPI application in
``app.main``.
"""
from fastapi import APIRouter

# Create a top t‑level router. Submodules will register their endpoints on this router.
router = APIRouter()
