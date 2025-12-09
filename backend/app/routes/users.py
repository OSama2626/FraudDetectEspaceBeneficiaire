# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from ..utils.auth import get_current_user
from ..core.db import get_db
from ..models.user import User

router = APIRouter()


class ProfileUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    imageUrl: Optional[str] = None


@router.get("/me")
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Route protégée pour tester l'authentification
    """
    return {
        "message": "Accès autorisé",
        "user_id": current_user.get("user_id"),
        "status": "authenticated"
    }


@router.put("/profile")
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile (name, image)"""
    clerk_id = current_user.get("user_id")
    if not clerk_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    db_user = db.query(User).filter(User.clerk_id == clerk_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if profile_data.firstName is not None:
        db_user.first_name = profile_data.firstName
    if profile_data.lastName is not None:
        db_user.last_name = profile_data.lastName
    if profile_data.imageUrl is not None:
        db_user.image_url = profile_data.imageUrl

    db.commit()
    db.refresh(db_user)

    return {"status": "success", "message": "Profile updated"}


@router.get("/sessions")
async def get_user_sessions(
    current_user: dict = Depends(get_current_user),
):
    """Get active sessions - placeholder (Clerk manages sessions)"""
    # Clerk handles session management; return empty or use Clerk Backend API
    return []


@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Revoke a session - placeholder (use Clerk Backend API if needed)"""
    return {"status": "success", "message": f"Session {session_id} revoked"}