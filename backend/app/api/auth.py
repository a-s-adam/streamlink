"""Authentication router for user management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.database import get_db
from ..models import User, UserCreate, UserRead
from ..config import get_settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/users", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        name=user_data.name,
        youtube_refresh_token=user_data.youtube_refresh_token
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/users", response_model=List[UserRead])
async def get_users(db: Session = Depends(get_db)):
    """Get all users (for development/testing)."""
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: str,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Update a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    user.email = user_data.email
    user.name = user_data.name
    if user_data.youtube_refresh_token:
        user.youtube_refresh_token = user_data.youtube_refresh_token
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}
