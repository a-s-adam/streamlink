"""Database seeding script for development and testing."""

import uuid
import logging
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from ..db.database import get_session_factory
from ..models import User, Provider, Item, Event, Embedding, Recommendation
from ..services.embeddings import get_embeddings_service

logger = logging.getLogger(__name__)


def seed_database():
    """Seed the database with sample data."""
    logger.info("Starting database seeding...")
    
    SessionLocal = get_session_factory()
    db = SessionLocal()
    
    try:
        # Create providers
        providers = create_providers(db)
        logger.info(f"Created {len(providers)} providers")
        
        # Create users
        users = create_users(db)
        logger.info(f"Created {len(users)} users")
        
        # Create items
        items = create_items(db)
        logger.info(f"Created {len(items)} items")
        
        # Create events
        events = create_events(db, users, items, providers)
        logger.info(f"Created {len(events)} events")
        
        # Create embeddings
        embeddings = create_embeddings(db, items)
        logger.info(f"Created {len(embeddings)} embeddings")
        
        # Create recommendations
        recommendations = create_recommendations(db, users, items)
        logger.info(f"Created {len(recommendations)} recommendations")
        
        db.commit()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_providers(db: Session) -> List[Provider]:
    """Create sample providers."""
    providers_data = [
        {
            "name": "NETFLIX",
            "display_name": "Netflix",
            "description": "Netflix streaming service",
            "is_active": True
        },
        {
            "name": "YOUTUBE",
            "display_name": "YouTube",
            "description": "YouTube video platform",
            "is_active": True
        }
    ]
    
    providers = []
    for data in providers_data:
        provider = Provider(**data)
        db.add(provider)
        providers.append(provider)
    
    db.commit()
    return providers


def create_users(db: Session) -> List[User]:
    """Create sample users."""
    users_data = [
        {
            "email": "demo@example.com",
            "name": "Demo User",
            "image": "https://example.com/avatar.jpg"
        }
    ]
    
    users = []
    for data in users_data:
        user = User(**data)
        db.add(user)
        users.append(user)
    
    db.commit()
    return users


def create_items(db: Session) -> List[Item]:
    """Create sample items."""
    items_data = [
        {
            "title": "Stranger Things",
            "source": "NETFLIX",
            "type": "tv_show",
            "year": 2016,
            "overview": "When a young boy disappears, his mother must confront terrifying forces in order to get him back.",
            "genres": ["Drama", "Fantasy", "Horror"],
            "runtime": 45,
            "poster_url": "https://example.com/stranger-things.jpg"
        },
        {
            "title": "The Crown",
            "source": "NETFLIX",
            "type": "tv_show",
            "year": 2016,
            "overview": "The story of Queen Elizabeth II and the events that shaped the second half of the 20th century.",
            "genres": ["Drama", "History"],
            "runtime": 58,
            "poster_url": "https://example.com/the-crown.jpg"
        },
        {
            "title": "Wednesday",
            "source": "NETFLIX",
            "type": "tv_show",
            "year": 2022,
            "overview": "Smart, sarcastic and a little dead inside, Wednesday Addams investigates a murder spree at her new school.",
            "genres": ["Comedy", "Crime", "Fantasy"],
            "runtime": 52,
            "poster_url": "https://example.com/wednesday.jpg"
        },
        {
            "title": "Black Mirror",
            "source": "NETFLIX",
            "type": "tv_show",
            "year": 2011,
            "overview": "An anthology series exploring a twisted, high-tech multiverse where humanity's greatest innovations and darkest instincts collide.",
            "genres": ["Drama", "Sci-Fi", "Thriller"],
            "runtime": 60,
            "poster_url": "https://example.com/black-mirror.jpg"
        },
        {
            "title": "Bridgerton",
            "source": "NETFLIX",
            "type": "tv_show",
            "year": 2020,
            "overview": "Wealth, lust, and betrayal set against the backdrop of Regency-era England.",
            "genres": ["Drama", "Romance"],
            "runtime": 62,
            "poster_url": "https://example.com/bridgerton.jpg"
        },
        {
            "title": "Python FastAPI Tutorial",
            "source": "YOUTUBE",
            "type": "video",
            "overview": "Learn how to build modern APIs with FastAPI and Python.",
            "genres": ["Education", "Technology"],
            "runtime": 45
        },
        {
            "title": "Machine Learning Basics",
            "source": "YOUTUBE",
            "type": "video",
            "overview": "Introduction to machine learning concepts and algorithms.",
            "genres": ["Education", "Technology"],
            "runtime": 60
        },
        {
            "title": "Docker for Beginners",
            "source": "YOUTUBE",
            "type": "video",
            "overview": "Learn Docker containerization from scratch.",
            "genres": ["Education", "Technology"],
            "runtime": 30
        }
    ]
    
    items = []
    for data in items_data:
        item = Item(**data)
        db.add(item)
        items.append(item)
    
    db.commit()
    return items


def create_events(db: Session, users: List[User], items: List[Item], providers: List[Provider]) -> List[Event]:
    """Create sample events."""
    events = []
    
    # Get provider IDs
    netflix_provider = next(p for p in providers if p.name == "NETFLIX")
    youtube_provider = next(p for p in providers if p.name == "YOUTUBE")
    
    # Create events for the demo user
    demo_user = users[0]
    
    # Netflix events (last 30 days)
    netflix_items = [item for item in items if item.source == "NETFLIX"]
    for i, item in enumerate(netflix_items):
        event = Event(
            user_id=demo_user.id,
            item_id=item.id,
            provider_id=netflix_provider.id,
            event_type="WATCHED",
            occurred_at=datetime.utcnow() - timedelta(days=i),
            raw={"duration": "45 min", "device": "TV"}
        )
        db.add(event)
        events.append(event)
    
    # YouTube events
    youtube_items = [item for item in items if item.source == "YOUTUBE"]
    for i, item in enumerate(youtube_items):
        event = Event(
            user_id=demo_user.id,
            item_id=item.id,
            provider_id=youtube_provider.id,
            event_type="WATCHED",
            occurred_at=datetime.utcnow() - timedelta(days=i+5),
            raw={"duration": "45 min", "device": "Computer"}
        )
        db.add(event)
        events.append(event)
    
    db.commit()
    return events


def create_embeddings(db: Session, items: List[Item]) -> List[Embedding]:
    """Create sample embeddings."""
    embeddings = []
    embeddings_service = get_embeddings_service()
    
    for item in items:
        # Generate embedding text
        embedding_text = f"{item.title}"
        if item.overview:
            embedding_text += f" {item.overview}"
        if item.genres:
            embedding_text += f" {' '.join(item.genres)}"
        
        # Generate mock embedding
        vector = embeddings_service._generate_mock_embedding(embedding_text)
        
        embedding = Embedding(
            item_id=item.id,
            vector=vector,
            model=embeddings_service.model_name,
            dimensions=len(vector)
        )
        
        db.add(embedding)
        embeddings.append(embedding)
    
    db.commit()
    return embeddings


def create_recommendations(db: Session, users: List[User], items: List[Item]) -> List[Recommendation]:
    """Create sample recommendations."""
    recommendations = []
    
    demo_user = users[0]
    
    # Create recommendations for the demo user
    for i, item in enumerate(items[:5]):  # Top 5 items
        recommendation = Recommendation(
            user_id=demo_user.id,
            item_id=item.id,
            score=0.9 - (i * 0.1),  # Decreasing scores
            reason=f"Based on your interest in {item.genres[0] if item.genres else 'similar content'}",
            algorithm="content_based"
        )
        
        db.add(recommendation)
        recommendations.append(recommendation)
    
    db.commit()
    return recommendations


if __name__ == "__main__":
    seed_database()
