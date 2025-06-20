from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean, Integer, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    


class Personal(Base):
    __tablename__ = "personals"

    uuid = Column(String, primary_key=True, index=True)  # UUID unique
    gender = Column(String,default=GenderEnum.MALE, nullable=True)
    professional_title = Column(String, index=True, nullable=True)
    title_description = Column(String,index=True, nullable=True )
    birth_date = Column(Date, index=True, nullable=True)
    place_of_birth = Column(String, index=True, nullable=True)
    region_of_origin = Column(String, index=True, nullable=True)
    adress = Column(String, index=True, nullable=True)
    nationality = Column(String, index=True, nullable=True)
    city = Column(String, index=True, nullable=True)
    country = Column(String, nullable=True)
    others = Column(String, nullable=True)



    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="personals")


    is_deleted = Column(Boolean,default=False)
    
    date_added  = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_modified = Column(DateTime, nullable=False, default=datetime.utcnow)

