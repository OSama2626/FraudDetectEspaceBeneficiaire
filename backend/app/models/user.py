# backend/app/models/user.py
from sqlalchemy import Column, String, Integer

# Importer 'Base' depuis son nouvel emplacement
# '..' signifie "remonter d'un dossier" (de models à app)
from ..core.db import Base 

class User(Base):
    """
    Modèle SQLAlchemy pour la table 'users'.
    Cette table stocke les utilisateurs synchronisés depuis Clerk.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # L'ID unique de l'utilisateur venant de Clerk (ex: "user_2j...")
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    image_url = Column(String)
    
    # Vous pouvez ajouter d'autres champs ici (ex: role, etc.)