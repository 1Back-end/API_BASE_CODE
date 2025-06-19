from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer,Enum as SQLEnum
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
    gender = Column(String,default=GenderEnum.MALE, nullable=False)
    professional_title = Column(String, index=True, nullable=False)
    title_description = Column(String,index=True, nullable=True )
    birth_date = Column(DateTime, index=True, nullable=False)
    place_of_birth = Column(String, index=True, nullable=False)
    region_of_origin = Column(String, index=True, nullable=False)
    adress = Column(String, index=True, nullable=False)
    nationality = Column(String, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    country = Column(String, nullable=False)
    others = Column(String, nullable=True)



    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="personals")


    is_deleted = Column(Boolean,default=False)
    
    date_added = date_added = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_modified = Column(DateTime, nullable=False, default=datetime.utcnow)

