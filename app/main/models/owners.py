from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM

class Ownerstatus(str,Enum):
    ACTIVED = "ACTIVED"
    UNACTIVED = "UNACTIVED"
    DELETED = "DELETED"
    BLOCKED= "BLOCKED"

class Owner(Base):
    """
     database model for storing Owner related details
    """
    __tablename__ = 'owners'

    uuid: str = Column(String, primary_key=True, unique=True)

    email: str = Column(String, nullable=False, default="")
    firstname: str = Column(String, nullable=False, default="")
    lastname: str = Column(String, nullable=False, default="")
    phone_number: str = Column(String(20), nullable=False, default="", index=True)
    
    added_by: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    creator = relationship("User", foreign_keys=[added_by], uselist=False)

    avatar_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid], uselist=False)
    
    
    password_hash: str = Column(String(100), nullable=True, default="")
    status = Column(String, index=True, nullable=False, default=Ownerstatus.UNACTIVED)
    is_deleted = Column(Boolean,default=False)


    date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())
    date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Owner: uuid: {} email: {}>'.format(self.uuid, self.email)


class OwnerActionValidation(Base):
    __tablename__ = 'owner_action_validations'

    uuid: str = Column(String, primary_key=True)

    user_uuid: str = Column(String, ForeignKey('owners.uuid'), nullable=True)
    code: str = Column(String, unique=False, nullable=True)
    expired_date: any = Column(DateTime, default=datetime.now())
    value: str = Column(String, default="", nullable=True)

    date_added: any = Column(DateTime, nullable=False, default=datetime.now())


