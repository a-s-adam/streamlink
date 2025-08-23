"""Recommendation model definitions.

This module defines the SQLAlchemy model for ``Recommendation`` which represents
user recommendations with scores and reasoning.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from ..db.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Why this was recommended
    algorithm: Mapped[str] = mapped_column(String, nullable=False, default="content_based")  # content_based, collaborative, hybrid
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    item = relationship("Item", back_populates="recommendations")


class RecommendationBase(BaseModel):
    user_id: uuid.UUID
    item_id: uuid.UUID
    score: float
    reason: Optional[str] = None
    algorithm: str = "content_based"


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationRead(RecommendationBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
