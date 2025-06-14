from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.main.models.db.base_class import Base

class Language(Base):
    __tablename__ = "languages"

    uuid = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
   

    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidate", back_populates="languages")

    is_deleted = Column(Boolean,default=False)
    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


