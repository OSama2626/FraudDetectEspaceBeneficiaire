# backend/app/security.py
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from clerk_sdk import ClerkClient
from clerk_sdk.errors import ClerkAPIException

# 1. Charger la clé secrète depuis le .env
CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")

if not CLERK_SECRET_KEY:
    raise EnvironmentError("La variable d'environnement CLERK_SECRET_KEY est manquante")

# 2. Initialiser le client Clerk
clerk_client = ClerkClient(secret_key=CLERK_SECRET_KEY)

# 3. Définir le schéma d'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dépendance FastAPI pour valider le token JWT de Clerk.
    """
    try:
        # 4. Valider le token
        session = clerk_client.sessions.verify_token(token)
        
        # Retourner l'ID utilisateur
        return { "user_id": session.user_id }
    
    except ClerkAPIException as e:
        # Token invalide
        print(f"Erreur de validation Clerk: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Erreur interne: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur",
        )