from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.main.models.db.base_class import Base

class Competence(Base):
    __tablename__ = "competences"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    level = Column(String, nullable=False)
    is_certified = Column(Boolean, default=False)  # anciennement certifiee
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)   # Ex : Informatique, Management, Communication
    date_added = Column(DateTime, default=datetime.utcnow)
    

    candidate_iuud = Column(Integer, ForeignKey("candidats.id"), nullable=False)
    candidate = relationship("Candidat", back_populates="competences")

    is_deleted = Column(Boolean, default=False)
