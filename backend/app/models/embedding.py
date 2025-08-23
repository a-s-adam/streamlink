"""Embedding model definitions.

This module defines the SQLAlchemy model for ``Embedding`` which represents
vector embeddings of media items for similarity search and recommendations.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel
from pgvector.sqlalchemy import Vector

from ..db.database import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False, index=True)
    vector: Mapped[Vector] = mapped_column(Vector(1536), nullable=False)  # pgvector column
    model: Mapped[str] = mapped_column(String, nullable=False, index=True)  # openai, ollama, etc.
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False, default=1536)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    item = relationship("Item", back_populates="embeddings")


class EmbeddingBase(BaseModel):
    item_id: uuid.UUID
    vector: List[float]
    model: str
    dimensions: int = 1536


class EmbeddingCreate(EmbeddingBase):
    pass


class EmbeddingRead(EmbeddingBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
