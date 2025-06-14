from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.main.models.db.base_class import Base

class Competence(Base):
    __tablename__ = "competences"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    is_certified = Column(Boolean, default=False)  # anciennement certifiee
    description = Column(String, nullable=True)
   

    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="competences")

    is_deleted = Column(Boolean,default=False)
    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


