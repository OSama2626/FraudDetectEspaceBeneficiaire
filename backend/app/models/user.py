# backend/app/models/user.py
from sqlalchemy import Column, String, Integer

# --- NOUVEAUX IMPORTS ---
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Optional
# -------------------------

# Importer 'Base' depuis son nouvel emplacement
from ..core.db import Base 

class User(Base):
    """
    Modèle SQLAlchemy (style 2.0) pour la table 'users'.
    """
    __tablename__ = "users"

    # --- NOUVELLE SYNTAXE ---
    # Utiliser Mapped et mapped_column
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    clerk_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    # Rendre les champs optionnels avec Optional[]
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    image_url: Mapped[Optional[str]] = mapped_column(String)
    # -------------------------