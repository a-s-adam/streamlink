"""User model definitions.

This module defines the SQLAlchemy model for ``User`` as well as related
Pydantic schemas for request/response bodies.  In the MVP we rely on Google
OAuth for authentication and store only minimal user information along with
encrypted refresh tokens for YouTube.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, EmailStr

from ..db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    youtube_refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    image: Optional[str] = None


class UserCreate(UserBase):
    youtube_refresh_token: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
