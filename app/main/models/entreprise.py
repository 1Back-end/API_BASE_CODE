from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum




class entreprise(Base):
    """
    Model representing a entreprise in the system.

    Attributes:
        id (str): Unique identifier for the entreprise.
        name (str): entreprise's name.
        email (str): entreprise's email address.
        role (str): User role (ADMIN or SUPER_ADMIN).
        industry (str): entreprise's industry.
        decription (str): entreprise's description.
        website (str): entreprise's website.
        created_at (datetime): Timestamp of account creation.
        
    """
    __tablename__ = "entreprise"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default=entrepriseRole.ADMIN)  # User role
    industry = Column(String(100))  # ex: Technologie, Finance, etc.
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)