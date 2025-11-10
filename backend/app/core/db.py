# backend/app/core/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Lire l'URL de la DB depuis votre fichier .env (à la racine de /backend)
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("ATTENTION: Toutes les variables d'environnement de la DB ne sont pas définies.")
    # Vous pouvez lever une exception ici si vous préférez
    # raise EnvironmentError("Variables de base de données manquantes dans .env")

# Format de l'URL pour PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    print(f"Erreur lors de la connexion à la base de données: {e}")
    # Gérer l'erreur de connexion comme vous le souhaitez

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir la Base ici. Tous vos modèles (comme User) l'importeront.
Base = declarative_base() 

def create_db_and_tables():
    """
    Crée toutes les tables dans la base de données
    qui héritent de 'Base'.
    """
    try:
        print("Création des tables (si elles n'existent pas)...")
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création des tables: {e}")

# Dépendance FastAPI pour obtenir une session DB dans vos routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()