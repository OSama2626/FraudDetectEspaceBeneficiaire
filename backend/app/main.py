# backend/app/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from dotenv import load_dotenv
from typing import Optional 
import pydantic
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# --- NOUVELLE APPROCHEClerk ---
from clerk_backend_api import Clerk, AuthenticateRequestOptions

# ----------------------------------------

# --- Chargement du .env ---
load_dotenv() 

# --- NOUVEAUX Imports (DB) ---
from .core.db import get_db, create_db_and_tables
from .models.user import User


# --- SECTION SÉCURITÉ AVEC clerk_backend_api ---
CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")
if not CLERK_SECRET_KEY:
    raise EnvironmentError("CLERK_SECRET_KEY est manquante dans .env")

# Initialisation du client Clerk
clerk_sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)

async def get_current_user(request: Request) -> dict:
    """
    Nouvelle dépendance FastAPI pour valider le token avec clerk_backend_api
    """
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173", "http://localhost:5174"],
                # jwt_key=os.getenv("JWT_KEY")  # Optionnel selon votre config
            )
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Non authentifié")

        user_id = request_state.payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="ID utilisateur manquant")

        return {"user_id": user_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur d'authentification Clerk: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur d'authentification: {str(e)}",
        )
# --- FIN SECTION SÉCURITÉ ---

# --- Modèle Pydantic (Schema) ---
class UserSync(pydantic.BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    imageUrl: Optional[str] = None
    email: Optional[str] = None

# --- Initialisation de l'App ---
app = FastAPI()

# --- Ajout du Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Créer les tables au démarrage ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables() 

# --- Route Publique ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FraudDetect (Publique)"}

# --- ROUTE AUTH CALLBACK (Version avec clerk_backend_api) ---
@app.post("/api/v1/auth/callback")
async def auth_callback(
    user_data: UserSync,
    request: Request,  # Ajout du request object
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Utilise la nouvelle dépendance
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
            db_user.email = user_data.email  # Mise à jour de l'email aussi
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

# --- Route de test pour vérifier l'authentification ---
@app.get("/api/v1/me")
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