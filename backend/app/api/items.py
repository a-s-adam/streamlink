"""Items router for managing media items."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db.database import get_db
from ..models import Item, ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[ItemRead])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get items with optional filtering and pagination."""
    query = db.query(Item)
    
    # Apply filters
    if source:
        query = query.filter(Item.source == source)
    
    if search:
        query = query.filter(Item.title.ilike(f"%{search}%"))
    
    # Apply pagination
    items = query.offset(skip).limit(limit).all()
    
    return items


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: str, db: Session = Depends(get_db)):
    """Get a specific item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@router.post("/", response_model=ItemRead)
async def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new item."""
    item = Item(**item_data.dict())
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: str,
    item_data: ItemCreate,
    db: Session = Depends(get_db)
):
    """Update an item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Update fields
    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: str, db: Session = Depends(get_db)):
    """Delete an item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully"}


@router.get("/stats/sources")
async def get_source_stats(db: Session = Depends(get_db)):
    """Get statistics about items by source."""
    from sqlalchemy import func
    
    stats = db.query(
        Item.source,
        func.count(Item.id).label("count")
    ).group_by(Item.source).all()
    
    return [{"source": source, "count": count} for source, count in stats]


@router.get("/stats/types")
async def get_type_stats(db: Session = Depends(get_db)):
    """Get statistics about items by type."""
    from sqlalchemy import func
    
    stats = db.query(
        Item.type,
        func.count(Item.id).label("count")
    ).group_by(Item.type).all()
    
    return [{"type": type_, "count": count} for type_, count in stats]
