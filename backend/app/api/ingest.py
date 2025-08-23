"""Ingestion router for Netflix CSV and YouTube data processing."""

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from ..db.database import get_db
from ..models import User
from ..celery_app import celery_app
from ..tasks.ingestion import ingest_netflix_csv, ingest_youtube_history
from ..services.youtube import YouTubeService

router = APIRouter(prefix="/ingest", tags=["ingestion"])


@router.post("/netflix")
async def upload_netflix_csv(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and process Netflix viewing history CSV."""
    # Validate file type
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are accepted"
        )
    
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # Read file content
        content = await file.read()
        csv_content = content.decode("utf-8")
        
        # Submit background task
        task = celery_app.send_task(
            "app.tasks.ingestion.ingest_netflix_csv",
            args=[str(user_id), csv_content]
        )
        
        return {
            "task_id": task.id,
            "status": "PENDING",
            "message": f"Netflix CSV upload started for {file.filename}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/youtube/start")
async def start_youtube_ingestion(
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Start YouTube OAuth flow for data ingestion."""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        youtube_service = YouTubeService()
        oauth_url = youtube_service.get_oauth_url()
        
        return {
            "oauth_url": oauth_url,
            "message": "YouTube OAuth flow initiated"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting YouTube ingestion: {str(e)}"
        )


@router.post("/youtube/callback")
async def youtube_oauth_callback(
    code: str = Form(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle YouTube OAuth callback and start ingestion."""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        youtube_service = YouTubeService()
        
        # Exchange code for tokens
        tokens = youtube_service.exchange_code_for_tokens(code)
        
        # Update user with refresh token
        user.youtube_refresh_token = tokens.get("refresh_token")
        db.commit()
        
        # Get viewing history
        history = youtube_service.get_viewing_history(tokens.get("access_token"))
        
        if not history:
            return {
                "message": "No viewing history found or API not available",
                "status": "completed"
            }
        
        # Submit background task for processing
        task = celery_app.send_task(
            "app.tasks.ingestion.ingest_youtube_history",
            args=[str(user_id), history]
        )
        
        return {
            "task_id": task.id,
            "status": "PENDING",
            "message": f"YouTube ingestion started with {len(history)} items"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing YouTube callback: {str(e)}"
        )


@router.post("/youtube/mock")
async def mock_youtube_ingestion(
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """Mock YouTube ingestion for testing without OAuth."""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        youtube_service = YouTubeService()
        history = youtube_service._get_mock_history()
        
        # Submit background task for processing
        task = celery_app.send_task(
            "app.tasks.ingestion.ingest_youtube_history",
            args=[str(user_id), history]
        )
        
        return {
            "task_id": task.id,
            "status": "PENDING",
            "message": f"Mock YouTube ingestion started with {len(history)} items"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting mock YouTube ingestion: {str(e)}"
        )


@router.get("/status/{task_id}")
async def get_ingestion_status(task_id: str):
    """Get the status of an ingestion task."""
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.ready():
            if task_result.successful():
                return {
                    "task_id": task_id,
                    "status": "SUCCESS",
                    "result": task_result.result
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "FAILURE",
                    "error": str(task_result.info)
                }
        else:
            return {
                "task_id": task_id,
                "status": task_result.state,
                "meta": task_result.info
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting task status: {str(e)}"
        )
