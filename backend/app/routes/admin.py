from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User, UserRole
from app.utils.auth import get_current_user

router = APIRouter(tags=["Admin"])


@router.post("/admin/check")
async def check_admin_status(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    clerk_id = current_user.get("user_id")
    user = db.query(User).filter(User.clerk_id == clerk_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    return {"admin": user.role == UserRole.ADMIN}
