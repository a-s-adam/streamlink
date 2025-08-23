"""Event model definitions.

This module defines the SQLAlchemy model for ``Event`` which represents
user interactions with media items (watched, liked, disliked, etc.).
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from ..db.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False, index=True)
    provider_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)  # WATCHED, LIKED, DISLIKED
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    raw: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # Store original data
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="events")
    item = relationship("Item", back_populates="events")
    provider = relationship("Provider", back_populates="events")


class EventBase(BaseModel):
    user_id: uuid.UUID
    item_id: uuid.UUID
    provider_id: uuid.UUID
    event_type: str
    occurred_at: datetime
    raw: Optional[Dict[str, Any]] = None


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
