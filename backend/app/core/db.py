import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus

# Lire les variables d'environnement
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("ATTENTION: Toutes les variables d'environnement de la DB ne sont pas définies.")
    raise EnvironmentError("Variables de base de données manquantes dans .env")

# Test de résolution DNS
try:
    ip_address = socket.gethostbyname(DB_HOST)
    print(f"✅ Hostname résolu: {DB_HOST} -> {ip_address}")
except socket.gaierror as e:
    print(f"❌ Erreur de résolution DNS pour {DB_HOST}: {e}")
    print("Vérifiez votre connexion Internet et les paramètres DNS")

# Encoder le mot de passe
encoded_password = quote_plus(DB_PASSWORD)

# Construire l'URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Tentative de connexion à: postgresql://{DB_USERNAME}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Teste la connexion avant utilisation
        connect_args={"connect_timeout": 10}  # Timeout de 10 secondes
    )
    
    # Tester la connexion immédiatement
    with engine.connect() as conn:
        print("✅ Connexion à la base de données réussie!")
        
except Exception as e:
    print(f"❌ Erreur de connexion à la base de données: {e}")
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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