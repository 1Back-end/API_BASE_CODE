from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Boolean,Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.main.models.db.base_class import Base


class Candidat(Base):
    __tablename__ = "candidates"

    uuid = Column(String, primary_key=True, index=True)  # UUID unique
    civility: str = Column(String, nullable=True, default="")
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)

    avatar_uuid = Column(String, ForeignKey('storages.uuid'), nullable=True)  # UUID de l'avatar
    avatar = relationship("Storage", foreign_keys=[avatar_uuid], uselist=False)  # Relation avec le modèle Storage pour l'avatar
    is_deleted = Column(Boolean,default=False)

    experiences = relationship("Experience", back_populates="candidate", cascade="all, delete-orphan")
    diplomas = relationship("Diploma", back_populates="candidate", cascade="all, delete-orphan")
    competences = relationship("Competence", back_populates="candidate", cascade="all, delete-orphan")


    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now())


class Experience(Base):
    __tablename__ = "experiences"

    uuid = Column(String, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)  # Exemple de date de début
    end_date = Column(String, nullable=True)  # Exemple de date de fin
    description = Column(Text, nullable=False)

    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="experiences")

    is_deleted = Column(Boolean, default=False)

    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now())

    @property
    def years_of_experience(self):
        """
        Calcule le nombre d'années d'expérience en fonction des dates de début et de fin.
        """
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")  # Assurez-vous que le format est correct
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d") if self.end_date else datetime.now()

        delta = end_date - start_date
        return delta.days // 365  # Convertir le nombre de jours en années


class Diploma(Base):
    __tablename__ = "diplomas"

    uuid = Column(String, primary_key=True, index=True)
    degree_name = Column(String, nullable=False)  # Nom du diplôme (ex: Bac, Master, Licence, etc.)
    institution_name = Column(String, nullable=False)  # Nom de l'institution où le diplôme a été obtenu
    start_year = Column(String, nullable=False)
    end_year = Column(String, nullable=False)
    address = Column(String, nullable=True)

    graduation_year = Column(String, nullable=False)  # Année d'obtention du diplôme

    candidate_uuid = Column(String, ForeignKey("candidates.uuid"), nullable=False)
    candidate = relationship("Candidat", back_populates="diplomas")

    is_deleted = Column(Boolean,default=False)

    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
