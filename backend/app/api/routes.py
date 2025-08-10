"""HTTP route declarations for the API layer.

All endpoints defined here are mounted under the ``/api`` prefix in the
FastAPI application.  At this stage these routes are simple stubs to be
implemented in later iterations.
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from pydantic import BaseModel

from ..config import Settings, get_settings

# Reuse the top ‑level router defined in app.api.__init__
from . import router


class UploadResponse(BaseModel):
    """Response returned after successfully enqueuing a file ingestion job."""
    task_id: str
    detail: str


@router.post(
    "/ingest/netflix",
    response_model=UploadResponse,
    summary="Upload a Netflix viewing history CSV",
)
async def ingest_netflix_csv(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> UploadResponse:
    """Accept a CSV file exported from Netflix and enqueue it for ingestion.

    In a later iteration this endpoint will store the file to disk and submit a
    background job to parse, enrich, and populate the knowledge graph and
    vector store.
    """
    # For now we simply read the filename and return a dummy task ID
    filename = file.filename
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are accepted")

    # TODO: Save file and enqueue background job
    task_id = "pending-task"
    return UploadResponse(task_id=task_id, detail=f"Received {filename}, ingestion not yet implemented")


@router.post(
    "/ingest/youtube/callback",
    summary="Handle the OAuth callback for YouTube ingestion",
)
async def youtube_oauth_callback(
    code: str,
    state: str | None = None,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    """Handle the OAuth2 callback from Google's consent screen for YouTube data.

    This stub records the authorization code and will exchange it for refresh
    and access tokens in a later iteration.
    """
    # TODO: Exchange code for tokens, save encrypted refresh token, enqueue ingestion
    return {"detail": f"YouTube OAuth callback received. Code: {code}, state: {state}"}


@router.get(
    "/recommendations",
    summary="Get recommendations for the authenticated user",
)
async def get_recommendations(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Return a list of recommended titles for the current user.

    This placeholder returns an empty list.  The actual implementation will blend
    graph based and embedding‑based recommendations and may call a local LLM for
    explanations if enabled.
    """
    # TODO: Retrieve user from session/auth token and compute recommendations
    return {"recommendations": "Not implemented"}
