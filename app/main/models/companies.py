from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean,Integer
from app.main.models.db.base_class import Base
from enum import Enum 


# Enum pour le statut de l'offre
class companiesStatut(str,Enum):
    active = "active"
    closed = "closed"
    expired = "expired"

class companies(Base):
    __tablename__ = "companies"

    uuid = Column(String, primary_key=True)  # Identifiant unique (UUID)
    name = Column(String, nullable=False)  # nom de l'entreprise
    description = Column(Text, nullable=False)  # Description détaillée
    industry = Column(String,nullable=False)  #  secteur d'activite 
    email = Column(String, unique=True, nullable=False)
    code_country = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    full_phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)  # Adresse du candidat
    website_url = Column(String,nullable=True )
    logo_url = Column(String, unique=True,nullable=True)
    status = Column(String,nullable=False, default=companiesStatut.active)  # Statut de l'entreprise (enum)
    is_deleted = Column(Boolean,default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    
