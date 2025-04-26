from dataclasses import dataclass 
from sqlalchemy.sql import func  
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM


# Enum pour le statut de l'offre
class profileStatus(str,Enum):
    pending  = "en attente"
    accepted = "retenu"
    rejected = "refuse"


class Profile(Base):
    __tablename__ = "profile"

    uuid = Column(String, primary_key=True)  # Identifiant unique (UUID)

    added_by: str = Column(String, ForeignKey('job_offers.uuid'), nullable=True)
    added_by: str = Column(String, ForeignKey('candidates.uuid'), nullable=True)
    

    submitted_date = Column(DateTime, default=func.now())  # Date de soumission 
    status = Column(String, nullable=False, default=profileStatus.EN ATTENTE)  # profil status
    reviewed by = Column(String,nullable=False)  # revu par 
    notes = Column(Text, nullable=False)  # commentaires 
    