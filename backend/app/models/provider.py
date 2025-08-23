"""Provider model definitions.

This module defines the SQLAlchemy model for ``Provider`` which represents
different data sources like Netflix, YouTube, etc.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from ..db.database import Base


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)  # NETFLIX, YOUTUBE, etc.
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[Optional[dict]] = mapped_column(Text, nullable=True)  # JSON config
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="provider")


class ProviderBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    is_active: bool = True
    config: Optional[dict] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderRead(ProviderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
