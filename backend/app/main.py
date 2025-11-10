# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import pydantic 
from typing import Optional 
import pandas as pd
import os

# --- NOUVEAU : Import pour CORS ---
from fastapi.middleware.cors import CORSMiddleware

# --- Chargement du .env ---
load_dotenv() 

# --- NOUVEAUX Imports (Auth & DB) ---
from .models.user import User 
from .core.db import get_db, create_db_and_tables

try:
    from .security import get_current_user
except ImportError:
    print("ATTENTION: 'app/security.py' n'a pas été trouvé. Les routes protégées échoueront.")
    async def get_current_user():
        raise HTTPException(status_code=500, detail="Fichier 'security.py' manquant")

# --- Modèle de données Pydantic (Schema) ---
class UserSync(pydantic.BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    imageUrl: Optional[str] = None
    email: Optional[str] = None

# --- Initialisation de l'App ---
app = FastAPI()

# --- AJOUT DU MIDDLEWARE CORS (ESSENTIEL) ---
# (Assurez-vous que le port est correct, :5173 est le port par défaut de Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # L'adresse de votre frontend React
    allow_credentials=True,                   # Autorise les cookies/tokens (comme Clerk)
    allow_methods=["*"],                      # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],                      # Autorise tous les en-têtes
)
# -----------------------------------------------

# --- Créer les tables au démarrage ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Route Publique ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FraudDetect (Publique)"}

# --- NOUVELLE ROUTE : AUTH CALLBACK (Sync-on-Login) ---
@app.post("/api/v1/auth/callback")
async def auth_callback(
    user_data: UserSync,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    clerk_id = current_user.get("user_id")

    if not clerk_id:
        raise HTTPException(status_code=401, detail="Utilisateur non valide depuis le token")

    db_user = db.query(User).filter(User.clerk_id == clerk_id).first()

    if db_user:
        db_user.first_name = user_data.firstName
        db_user.last_name = user_data.lastName
        db_user.image_url = user_data.imageUrl
        print(f"Utilisateur mis à jour : {clerk_id}")
    else:
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
    
    return {"status": "success", "message": "Utilisateur synchronisé"}

