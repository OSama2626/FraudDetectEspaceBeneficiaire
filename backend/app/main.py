from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv # Needed for loading .env variables
# Import all route modules needed for both features
from app.routes import checks # Route for Beneficiary checks
from app.routes import auth, users 
from app.routes import admin, webhooks
from app.routes import cheques  # Real cheques from Supabase



# --- Chargement du .env (doit être appelé avant d'importer les modules qui lisent les variables) ---
load_dotenv()

# Imports de la logique de l'application
from .core.db import create_db_and_tables

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

# --- Événement de démarrage (From HEAD) ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- INCLURE LES ROUTEURS ---
# Include all routes defined in auth.py (Authentication)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# Include all routes defined in users.py (User management)
app.include_router(users.router, prefix="/auth", tags=["Users"])
# Include all routes defined in checks.py (Beneficiary Espace)
app.include_router(checks.router, tags=["Checks"])

# Include cheques routes (real data from Supabase)
app.include_router(cheques.router, prefix="/cheques", tags=["Cheques"])

# Include Clerk webhook handler
app.include_router(webhooks.router, prefix="/webhooks")

# Include admin helpers
app.include_router(admin.router)

# --- Route Publique ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FraudDetect (Publique)"}