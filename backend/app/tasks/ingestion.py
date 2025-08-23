"""Ingestion tasks for processing Netflix CSV and YouTube data."""

import csv
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from io import StringIO

from celery import current_task
from sqlalchemy.orm import Session

from app.db.database import get_session_factory
from app.models import User, Item, Event, Provider
from app.services.netflix_csv import NetflixCSVParser
from app.services.youtube import YouTubeService

logger = logging.getLogger(__name__)


def ingest_netflix_csv(user_id: str, csv_content: str) -> Dict[str, Any]:
    """Process Netflix CSV content and create items and events."""
    try:
        current_task.update_state(state="PROCESSING", meta={"progress": 0})
        
        # Parse CSV content
        parser = NetflixCSVParser()
        items_data = parser.parse_csv(csv_content)
        
        current_task.update_state(state="PROCESSING", meta={"progress": 30})
        
        # Get database session
        SessionLocal = get_session_factory()
        db = SessionLocal()
        
        try:
            # Get or create Netflix provider
            provider = db.query(Provider).filter(Provider.name == "NETFLIX").first()
            if not provider:
                provider = Provider(
                    name="NETFLIX",
                    display_name="Netflix",
                    description="Netflix streaming service"
                )
                db.add(provider)
                db.commit()
                db.refresh(provider)
            
            # Process each item
            created_items = []
            created_events = []
            
            for i, item_data in enumerate(items_data):
                # Check if item already exists
                existing_item = db.query(Item).filter(
                    Item.title == item_data["title"],
                    Item.year == item_data.get("year"),
                    Item.source == "NETFLIX"
                ).first()
                
                if existing_item:
                    item = existing_item
                else:
                    # Create new item
                    item = Item(
                        external_id=item_data.get("external_id"),
                        source="NETFLIX",
                        title=item_data["title"],
                        year=item_data.get("year"),
                        type="movie" if item_data.get("type") == "movie" else "tv_show",
                        created_at=datetime.utcnow()
                    )
                    db.add(item)
                    db.commit()
                    db.refresh(item)
                    created_items.append(item)
                
                # Create event
                event = Event(
                    user_id=user_id,
                    item_id=item.id,
                    provider_id=provider.id,
                    event_type="WATCHED",
                    occurred_at=item_data.get("date", datetime.utcnow()),
                    raw=item_data,
                    created_at=datetime.utcnow()
                )
                db.add(event)
                created_events.append(event)
                
                # Update progress
                progress = 30 + int((i + 1) / len(items_data) * 60)
                current_task.update_state(
                    state="PROCESSING", 
                    meta={"progress": progress, "processed": i + 1, "total": len(items_data)}
                )
            
            db.commit()
            
            current_task.update_state(state="PROCESSING", meta={"progress": 90})
            
            # Trigger enrichment task
            from app.tasks.enrichment import enrich_item_metadata
            for item in created_items:
                enrich_item_metadata.delay(str(item.id))
            
            current_task.update_state(state="SUCCESS", meta={"progress": 100})
            
            return {
                "status": "success",
                "items_created": len(created_items),
                "events_created": len(created_events),
                "message": f"Successfully processed {len(items_data)} Netflix items"
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error processing Netflix CSV: {str(e)}")
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise


def ingest_youtube_history(user_id: str, history_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process YouTube history data and create items and events."""
    try:
        current_task.update_state(state="PROCESSING", meta={"progress": 0})
        
        # Get database session
        SessionLocal = get_session_factory()
        db = SessionLocal()
        
        try:
            # Get or create YouTube provider
            provider = db.query(Provider).filter(Provider.name == "YOUTUBE").first()
            if not provider:
                provider = Provider(
                    name="YOUTUBE",
                    display_name="YouTube",
                    description="YouTube video platform"
                )
                db.add(provider)
                db.commit()
                db.refresh(provider)
            
            # Process each history item
            created_items = []
            created_events = []
            
            for i, history_item in enumerate(history_data):
                # Extract video title from "Watched" format
                title = history_item.get("title", "")
                if title.startswith("Watched "):
                    title = title[8:].strip('"')
                
                # Skip if not a video
                if not title or "YouTube" in title:
                    continue
                
                # Check if item already exists
                existing_item = db.query(Item).filter(
                    Item.title == title,
                    Item.source == "YOUTUBE"
                ).first()
                
                if existing_item:
                    item = existing_item
                else:
                    # Create new item
                    item = Item(
                        external_id=history_item.get("titleUrl", "").split("=")[-1] if "=" in history_item.get("titleUrl", "") else None,
                        source="YOUTUBE",
                        title=title,
                        type="video",
                        created_at=datetime.utcnow()
                    )
                    db.add(item)
                    db.commit()
                    db.refresh(item)
                    created_items.append(item)
                
                # Create event
                event = Event(
                    user_id=user_id,
                    item_id=item.id,
                    provider_id=provider.id,
                    event_type="WATCHED",
                    occurred_at=datetime.fromisoformat(history_item.get("time", "").replace("Z", "+00:00")),
                    raw=history_item,
                    created_at=datetime.utcnow()
                )
                db.add(event)
                created_events.append(event)
                
                # Update progress
                progress = int((i + 1) / len(history_data) * 80)
                current_task.update_state(
                    state="PROCESSING", 
                    meta={"progress": progress, "processed": i + 1, "total": len(history_data)}
                )
            
            db.commit()
            
            current_task.update_state(state="PROCESSING", meta={"progress": 90})
            
            # Trigger enrichment task for new items
            from app.tasks.enrichment import enrich_item_metadata
            for item in created_items:
                enrich_item_metadata.delay(str(item.id))
            
            current_task.update_state(state="SUCCESS", meta={"progress": 100})
            
            return {
                "status": "success",
                "items_created": len(created_items),
                "events_created": len(created_events),
                "message": f"Successfully processed {len(history_data)} YouTube history items"
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error processing YouTube history: {str(e)}")
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise
