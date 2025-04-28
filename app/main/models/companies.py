from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum


class CompanyStatus(str,Enum):
    ACTIVE = "ACTIVE",
    INACTIVE = "INACTIVE",
    CLOSED = "CLOSED"

class CompanyType(str,Enum):
    PERSONNAL = "PERSONNAL",
    SARL = "SARL"
    SA = "SA"
    SAS = "SAS"
    ONG = "ONG"
    

class Company(Base):
    __tablename__ = "companies"

    uuid = Column(String,primary_key=True,index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    phone = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    slogan = Column(String, nullable=True)

    address_uuid = Column(String, ForeignKey('addresses.uuid'), nullable=True)
    address = relationship("Address",foreign_keys=[address_uuid])
    
    logo_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    logo = relationship("Storage", foreign_keys=[logo_uuid])

    signature_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    signature = relationship("Storage", foreign_keys=[signature_uuid])

    stamp_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    stamp = relationship("Storage", foreign_keys=[stamp_uuid])

    founded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    employee_count = Column(Integer, default=0)
    type = Column(String, nullable=False,default=CompanyType.PERSONNAL)
    status = Column(String,nullable=False, default=CompanyStatus.INACTIVE)

    website = Column(String, nullable=True)

    added_by = Column(String, ForeignKey("owners.uuid"), nullable=False)  # Référence au propriétaire
    owner = relationship("Owner", foreign_keys=[added_by])

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"Company(name='{self.name}', email='{self.email}', phone='{self.phone}', status='{self.status}', type='{self.type}', added_by='{self.added_by}')"