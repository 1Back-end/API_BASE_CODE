from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.main.models.db.base_class import Base




class Media(Base):
    __tablename__ = "medias"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)

    
    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="medias")


    is_deleted = Column(Boolean,default=False)
    
    date_added = date_added = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_modified = Column(DateTime, nullable=False, default=datetime.utcnow)
