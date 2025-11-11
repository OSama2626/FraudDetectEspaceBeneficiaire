# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

# Imports depuis notre application
from ..core.db import get_db
from ..utils.auth import get_current_user # <-- Import de la dépendance
from ..models.user import User
from ..schemas.user import UserSync      # <-- Import du schema

# Création d'un routeur
router = APIRouter()

@router.post("/callback")
async def auth_callback(
    user_data: UserSync,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # <-- Utilise la dépendance
):
    clerk_id = current_user.get("user_id")
    if not clerk_id:
        raise HTTPException(status_code=401, detail="Utilisateur non valide depuis le token")

    try:
        # 1. Vérifier si l'utilisateur existe
        db_user = db.query(User).filter(User.clerk_id == clerk_id).first()

        if db_user:
            # 2. L'utilisateur existe, on le MET À JOUR
            db_user.first_name = user_data.firstName
            db_user.last_name = user_data.lastName
            db_user.image_url = user_data.imageUrl
            db_user.email = user_data.email
            print(f"Utilisateur mis à jour : {clerk_id}")
        else:
            # 3. L'utilisateur n'existe pas, on le CRÉE
            new_user = User(
                clerk_id=clerk_id,
                email=user_data.email,
                first_name=user_data.firstName,
                last_name=user_data.lastName,
                image_url=user_data.imageUrl
            )
            db.add(new_user)
            print(f"Nouvel utilisateur créé : {clerk_id}")
        
        db.commit()
        return {
            "status": "success",
            "message": "Utilisateur synchronisé",
            "clerk_id": clerk_id
        }

    except Exception as e:
        db.rollback()
        print(f"Erreur SQLAlchemy: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de base de données: {str(e)}")