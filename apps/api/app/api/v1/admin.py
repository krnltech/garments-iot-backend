"""
Admin API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

from ...db.database import get_db
from ...schemas.user import UserResponse
from ...crud import user as user_crud
from ...services.auth import get_current_admin_user
from ...models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    try:
        users = user_crud.get_all_users(db)
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
