"""Database connection and session management.

This module defines a SQLAlchemy engine and a session factory based on the
``DATABASE_URL`` environment variable.  It also provides a ``Base`` class for
declarative models and a ``get_db`` dependency for FastAPI routes.
"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from ..config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""
    pass


def _create_engine():
    settings = get_settings()
    # Add pgvector support
    engine = create_engine(
        settings.database_url, 
        pool_pre_ping=True,
        echo=settings.app_env == "development"
    )
    
    # Import pgvector extension
    try:
        from pgvector.sqlalchemy import Vector
        # This ensures pgvector is available
    except ImportError:
        pass
    
    return engine


# The engine is created lazily to allow settings to be loaded
_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = _create_engine()
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy session and ensures it is closed.
    
    Usage:

    ```python
    @router.get("/items")
    def read_items(db: Session = Depends(get_db)):
        ...
    ```
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables (for development/testing)
def create_tables():
    """Create all tables. Use only for development/testing."""
    Base.metadata.create_all(bind=get_engine())


def drop_tables():
    """Drop all tables. Use only for development/testing."""
    Base.metadata.drop_all(bind=get_engine())
