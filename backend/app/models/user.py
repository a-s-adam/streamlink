"""User model definitions.

This module defines the SQLAlchemy model for ``User`` as well as related
Pydantic schemas for request/response bodies.  In the MVP we rely on Google
OAuth for authentication and store only minimal user information along with
encrypted refresh tokens for YouTube.
"""
import uuid
from typing import Optional

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, EmailStr

from ..db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    youtube_refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] | None = None


class UserCreate(UserBase):
    youtube_refresh_token: Optional[str] | None = None


class UserRead(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
