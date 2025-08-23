"""Recommendations router for user recommendations."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db.database import get_db
from ..models import Recommendation, RecommendationRead, Item, ItemRead
from ..celery_app import celery_app

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=List[dict])
async def get_recommendations(
    user_id: str = Query(...),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recommendations for a user."""
    # Get user's recommendations
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.score.desc()).limit(limit).all()
    
    if not recommendations:
        return []
    
    # Get item details for each recommendation
    item_ids = [rec.item_id for rec in recommendations]
    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    
    # Create item lookup
    item_lookup = {str(item.id): item for item in items}
    
    # Combine recommendation and item data
    result = []
    for rec in recommendations:
        item = item_lookup.get(str(rec.item_id))
        if item:
            result.append({
                "id": str(rec.id),
                "score": rec.score,
                "reason": rec.reason,
                "algorithm": rec.algorithm,
                "created_at": rec.created_at,
                "item": {
                    "id": str(item.id),
                    "title": item.title,
                    "source": item.source,
                    "type": item.type,
                    "year": item.year,
                    "poster_url": item.poster_url,
                    "overview": item.overview,
                    "genres": item.genres,
                    "runtime": item.runtime
                }
            })
    
    return result


@router.post("/refresh")
async def refresh_recommendations(
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Refresh recommendations for a user."""
    try:
        # Submit background task
        task = celery_app.send_task(
            "app.tasks.recommendations.refresh_user_recommendations",
            args=[user_id]
        )
        
        return {
            "task_id": task.id,
            "status": "PENDING",
            "message": "Recommendation refresh started"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting recommendation refresh: {str(e)}"
        )


@router.get("/status/{task_id}")
async def get_recommendation_status(task_id: str):
    """Get the status of a recommendation task."""
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


@router.get("/similar/{item_id}")
async def get_similar_items(
    item_id: str,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get items similar to a specific item."""
    # Get the target item
    target_item = db.query(Item).filter(Item.id == item_id).first()
    if not target_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # For now, return items with similar genres or type
    # In a full implementation, this would use vector similarity
    similar_items = db.query(Item).filter(
        Item.id != item_id,
        Item.type == target_item.type
    ).limit(limit).all()
    
    return [
        {
            "id": str(item.id),
            "title": item.title,
            "source": item.source,
            "type": item.type,
            "year": item.year,
            "poster_url": item.poster_url,
            "overview": item.overview,
            "genres": item.genres,
            "runtime": item.runtime
        }
        for item in similar_items
    ]


@router.get("/stats/{user_id}")
async def get_recommendation_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get recommendation statistics for a user."""
    from sqlalchemy import func
    
    # Count recommendations by algorithm
    algo_stats = db.query(
        Recommendation.algorithm,
        func.count(Recommendation.id).label("count"),
        func.avg(Recommendation.score).label("avg_score")
    ).filter(
        Recommendation.user_id == user_id
    ).group_by(Recommendation.algorithm).all()
    
    # Get recent recommendations
    recent_recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.created_at.desc()).limit(5).all()
    
    return {
        "algorithm_stats": [
            {
                "algorithm": algo,
                "count": count,
                "average_score": float(avg_score) if avg_score else 0.0
            }
            for algo, count, avg_score in algo_stats
        ],
        "recent_recommendations": len(recent_recommendations),
        "total_recommendations": sum(count for _, count, _ in algo_stats)
    }
