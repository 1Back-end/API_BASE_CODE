from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.main.models.db.base_class import Base

class Hobby(Base):
    __tablename__ = "hobbies"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
   

    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="hobbies")

    is_deleted = Column(Boolean,default=False)

    date_added = date_added = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_modified = Column(DateTime, nullable=False, default=datetime.utcnow)

