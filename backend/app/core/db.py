# backend/app/core/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase # <== Style 2.0
from urllib.parse import quote_plus # Pour les mots de passe

# Lire l'URL de la DB depuis votre fichier .env
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("ATTENTION: Toutes les variables d'environnement de la DB ne sont pas définies.")
    raise EnvironmentError("Variables de base de données manquantes dans .env")

# Encoder le mot de passe s'il contient des caractères spéciaux
encoded_password = quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Tentative de connexion à: postgresql://{DB_USERNAME}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    # Tester la connexion
    with engine.connect() as conn:
        print("✅ Connexion à la base de données (SQLAlchemy) réussie!")
except Exception as e:
    print(f"❌ Erreur de connexion (SQLAlchemy): {e}")
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Définir la Base
class Base(DeclarativeBase):
    pass

def create_db_and_tables():
    if engine is None:
        print("❌ Impossible de créer les tables: moteur de base de données non disponible")
        return
    try:
        print("Création des tables (si elles n'existent pas)...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")

def get_db():
    if engine is None:
        raise Exception("Base de données non disponible")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()