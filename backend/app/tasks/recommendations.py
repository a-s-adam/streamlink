"""Recommendations tasks for generating user recommendations."""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import numpy as np

from celery import current_task
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_session_factory
from app.models import User, Item, Event, Embedding, Recommendation
from app.services.embeddings import get_embeddings_service

logger = logging.getLogger(__name__)


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


def refresh_user_recommendations(user_id: str) -> Dict[str, Any]:
    """Generate new recommendations for a user."""
    try:
        current_task.update_state(state="PROCESSING", meta={"progress": 0})
        
        # Get database session
        SessionLocal = get_session_factory()
        db = SessionLocal()
        
        try:
            # Get user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            current_task.update_state(state="PROCESSING", meta={"progress": 20})
            
            # Get user's watched items from the last 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            user_events = db.query(Event).filter(
                Event.user_id == user_id,
                Event.event_type == "WATCHED",
                Event.occurred_at >= thirty_days_ago
            ).all()
            
            if not user_events:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "no_data", "message": "No recent viewing data"}
            
            current_task.update_state(state="PROCESSING", meta={"progress": 40})
            
            # Get embeddings for watched items
            watched_item_ids = [event.item_id for event in user_events]
            watched_embeddings = db.query(Embedding).filter(
                Embedding.item_id.in_(watched_item_ids)
            ).all()
            
            if not watched_embeddings:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "no_embeddings", "message": "No embeddings for watched items"}
            
            # Calculate user's preference vector (centroid of watched items)
            vectors = [emb.vector for emb in watched_embeddings]
            user_preference = np.mean(vectors, axis=0)
            
            current_task.update_state(state="PROCESSING", meta={"progress": 60})
            
            # Get all items with embeddings (excluding watched ones)
            all_embeddings = db.query(Embedding).filter(
                ~Embedding.item_id.in_(watched_item_ids)
            ).all()
            
            if not all_embeddings:
                current_task.update_state(state="SUCCESS", meta={"progress": 100})
                return {"status": "no_candidates", "message": "No candidate items for recommendations"}
            
            # Calculate similarities
            similarities = []
            for emb in all_embeddings:
                similarity = cosine_similarity(user_preference, emb.vector)
                similarities.append((emb.item_id, similarity))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            current_task.update_state(state="PROCESSING", meta={"progress": 80})
            
            # Remove old recommendations
            db.query(Recommendation).filter(
                Recommendation.user_id == user_id
            ).delete()
            
            # Create new recommendations (top 20)
            new_recommendations = []
            for item_id, score in similarities[:20]:
                recommendation = Recommendation(
                    user_id=user_id,
                    item_id=item_id,
                    score=float(score),
                    reason="Based on your recent viewing history",
                    algorithm="content_based",
                    created_at=datetime.utcnow()
                )
                new_recommendations.append(recommendation)
            
            db.add_all(new_recommendations)
            db.commit()
            
            current_task.update_state(state="SUCCESS", meta={"progress": 100})
            
            return {
                "status": "success",
                "recommendations_created": len(new_recommendations),
                "message": f"Successfully generated {len(new_recommendations)} recommendations"
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {str(e)}")
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)
