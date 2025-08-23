"""Item model definitions.

This module defines the SQLAlchemy model for ``Item`` which represents
media items (movies, TV shows, YouTube videos) with their metadata.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, DateTime, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from ..db.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    source: Mapped[str] = mapped_column(String, nullable=False, index=True)  # NETFLIX, YOUTUBE, etc.
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=False, default="movie")  # movie, tv_show, video
    poster_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    runtime: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    tmdb_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="item")
    embeddings = relationship("Embedding", back_populates="item")
    recommendations = relationship("Recommendation", back_populates="item")


class ItemBase(BaseModel):
    external_id: Optional[str] = None
    source: str
    title: str
    year: Optional[int] = None
    type: str = "movie"
    poster_url: Optional[str] = None
    overview: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    tmdb_id: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
