"""Enrichment tasks for TMDB metadata and embeddings."""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from celery import current_task
from sqlalchemy.orm import Session

from app.db.database import get_session_factory
from app.models import Item, Embedding
from app.services.tmdb import TMDBService
from app.services.embeddings import get_embeddings_service

logger = logging.getLogger(__name__)


def enrich_item_metadata(item_id: str) -> Dict[str, Any]:
    """Enrich item with TMDB metadata."""
    try:
        current_task.update_state(state="PROCESSING", meta={"progress": 0})
        
        # Get database session
        SessionLocal = get_session_factory()
        db = SessionLocal()
        
        try:
            # Get item
            item = db.query(Item).filter(Item.id == item_id).first()
            if not item:
                raise ValueError(f"Item {item_id} not found")
            
            current_task.update_state(state="PROCESSING", meta={"progress": 20})
            
            # Skip if already enriched
            if item.tmdb_id and item.overview:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "skipped", "message": "Item already enriched"}
            
            # Get TMDB service
            tmdb_service = TMDBService()
            
            # Search for item
            search_results = tmdb_service.search_item(item.title, item.year)
            
            if not search_results:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "no_results", "message": "No TMDB results found"}
            
            # Use first result
            tmdb_item = search_results[0]
            
            current_task.update_state(state="PROCESSING", meta={"progress": 60})
            
            # Update item with TMDB data
            item.tmdb_id = str(tmdb_item["id"])
            item.overview = tmdb_item.get("overview")
            item.poster_url = tmdb_item.get("poster_path")
            item.genres = [genre["name"] for genre in tmdb_item.get("genres", [])]
            item.runtime = tmdb_item.get("runtime")
            item.updated_at = datetime.utcnow()
            
            db.commit()
            
            current_task.update_state(state="PROCESSING", meta={"progress": 80})
            
            # Trigger embedding generation
            from app.tasks.recommendations import generate_item_embedding
            generate_item_embedding.delay(str(item.id))
            
            current_task.update_state(state="SUCCESS", meta={"progress": 100})
            
            return {
                "status": "success",
                "tmdb_id": item.tmdb_id,
                "message": f"Successfully enriched item {item.title}"
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error enriching item {item_id}: {str(e)}")
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise


def generate_item_embedding(item_id: str) -> Dict[str, Any]:
    """Generate embedding for an item."""
    try:
        current_task.update_state(state="PROCESSING", meta={"progress": 0})
        
        # Get database session
        SessionLocal = get_session_factory()
        db = SessionLocal()
        
        try:
            # Get item
            item = db.query(Item).filter(Item.id == item_id).first()
            if not item:
                raise ValueError(f"Item {item_id} not found")
            
            current_task.update_state(state="PROCESSING", meta={"progress": 20})
            
            # Check if embedding already exists
            existing_embedding = db.query(Embedding).filter(
                Embedding.item_id == item.id
            ).first()
            
            if existing_embedding:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "skipped", "message": "Embedding already exists"}
            
            # Get embeddings service
            embeddings_service = get_embeddings_service()
            
            current_task.update_state(state="PROCESSING", meta={"progress": 40})
            
            # Generate embedding text
            embedding_text = f"{item.title}"
            if item.overview:
                embedding_text += f" {item.overview}"
            if item.genres:
                embedding_text += f" {' '.join(item.genres)}"
            
            # Generate embedding
            vector = embeddings_service.generate_embedding(embedding_text)
            
            current_task.update_state(state="PROCESSING", meta={"progress": 80})
            
            # Store embedding
            embedding = Embedding(
                item_id=item.id,
                vector=vector,
                model=embeddings_service.model_name,
                dimensions=len(vector),
                created_at=datetime.utcnow()
            )
            
            db.add(embedding)
            db.commit()
            
            current_task.update_state(state="SUCCESS", meta={"progress": 100})
            
            return {
                "status": "success",
                "dimensions": len(vector),
                "model": embeddings_service.model_name,
                "message": f"Successfully generated embedding for {item.title}"
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error generating embedding for item {item_id}: {str(e)}")
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise
