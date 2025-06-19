from http import client
import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from app.main.core.security import generate_password, get_password_hash,verify_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas
from app.main.core.mail import send_account_creation_email
import requests
# import tldextract
# import openai
import urllib3
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
# load_dotenv()
# # Récupérer la clé API OpenAI depuis les variables d'environnement
# openai.api_key = os.getenv("OPENAI_API_KEY")
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CRUDCandidat(CRUDBase[models.Candidat,schemas.CandidateBase,schemas.CandidateCreate]):
    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Candidat).filter(models.Candidat.email==email).first()
    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Candidat).filter(models.Candidat.phone_number==phone_number).first()
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Candidat).filter(models.Candidat.uuid==uuid).first()


    @classmethod
    def create(cls, db: Session, *, candidate: schemas.CandidateCreate):
        commdon_uuid = str(uuid.uuid4())
        # Créer le candidat
        db_candidate = models.Candidat(
            uuid=commdon_uuid,
            civility=candidate.civility,
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            email=candidate.email,
            phone_number=candidate.phone_number,
        )
        db.add(db_candidate)
        db.commit()
        new_user = models.User(
            uuid = commdon_uuid,
            first_name = candidate.first_name,
            last_name = candidate.last_name,
            email = candidate.email,
            password_hash=get_password_hash(candidate.password),
            role = models.UserRole.CANDIDATE
        )
        db.add(new_user)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate





    @classmethod
    def get_my_experiences_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Experience).filter(models.Experience.uuid==uuid,models.Experience.is_deleted==False).first()

    @classmethod
    def create_experiences(cls,db:Session,experiences:schemas.ExperenciesCreate,candidate_uuid:str):
        obj_in = models.Experience(
            uuid = str(uuid.uuid4()),
            job_title = experiences.job_title,
            company_name = experiences.company_name,
            start_date = experiences.start_date,
            end_date = experiences.end_date,
            description = experiences.description,
            candidate_uuid = candidate_uuid,
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    @classmethod
    def update_experiences(cls,db:Session,*,experiences:schemas.ExperenciesUpdate,candidate_uuid:str):
        db_obj = cls.get_my_experiences_by_uuid(db,uuid=experiences.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="experience-not-found"))

        db_obj.job_title = experiences.job_title if experiences.job_title else db_obj.job_title
        db_obj.company_name = experiences.company_name if experiences.company_name else db_obj.company_name
        db_obj.start_date = experiences.start_date if experiences.start_date else db_obj.start_date
        db_obj.end_date = experiences.end_date if experiences.end_date else db_obj.end_date
        db_obj.description = experiences.description if experiences.description else db_obj.description
        db_obj.candidate_uuid = experiences.candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_my_experiences(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            candidate_uuid: Optional[str] = None,
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Experience).filter(models.Experience.candidate_uuid == candidate_uuid,
                                                       models.Experience.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Experience.start_date.ilike(f'%{keyword}%'),
                    models.Experience.end_date.ilike(f'%{keyword}%'),
                    models.Experience.company_name.ilike(f'%{keyword}%'),
                    models.Experience.job_title.ilike(f'%{keyword}%'),
                    models.Experience.description.ilike(f'%{keyword}%'),
                )
            )

        if order and order_field and hasattr(models.Experience, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Experience, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Experience, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.ExperiencesResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


    @classmethod
    def create_diplomas(cls,db:Session,*,diploma:schemas.DiplomaCreate,candidate_uuid:str):
        obj_in = models.Diploma(
            uuid = str(uuid.uuid4()),
            degree_name = diploma.degree_name,
            institution_name = diploma.institution_name,
            start_year = diploma.start_year,
            end_year= diploma.end_year,
            graduation_year = f"{diploma.start_year}/{diploma.end_year}",
            candidate_uuid = candidate_uuid,
            address = diploma.address,
        )
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    @classmethod
    def get_diploma_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Diploma).filter(models.Diploma.uuid==uuid,models.Diploma.is_deleted==False).first()

    @classmethod
    def update_diplomas(cls,db:Session,*,obj_in:schemas.DiplomaUpdate,candidate_uuid:str):
        db_obj = cls.get_diploma_by_uuid(db,uuid=obj_in.uuid)

        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="diploma-not-found"))

        db_obj.degree_name = obj_in.degree_name if obj_in.degree_name else db_obj.degree_name
        db_obj.institution_name = obj_in.institution_name if obj_in.institution_name else db_obj.institution_name
        db_obj.address = obj_in.address if obj_in.address else db_obj.address
        db_obj.start_year = obj_in.start_year if obj_in.start_year else db_obj.start_year
        db_obj.end_year = obj_in.end_year if obj_in.end_year else db_obj.end_year
        db_obj.graduation_year = f"{obj_in.start_year}/{obj_in.end_year}"
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def delete_diplomas(cls,db:Session,*,uuid:str):
        db_obj = cls.get_diploma_by_uuid(db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="diploma-not-found"))
        db_obj.is_deleted = True
        db.commit()

    @classmethod
    def delete_experiences(cls,db:Session,*,uuid:str):
        db_obj = cls.get_my_experiences_by_uuid(db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="experience-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def get_my_diplomas(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            candidate_uuid: Optional[str] = None,
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Diploma).filter(models.Diploma.candidate_uuid==candidate_uuid,models.Diploma.is_deleted==False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Diploma.address.ilike(f'%{keyword}%'),
                    models.Diploma.degree_name.ilike(f'%{keyword}%'),
                    models.Diploma.graduation_year.ilike(f'%{keyword}%'),
                    models.Diploma.institution_name.ilike(f'%{keyword}%'),
                    models.Diploma.start_year.ilike(f'%{keyword}%'),
                    models.Diploma.end_year.ilike(f'%{keyword}%'),

                )
            )

        if order and order_field and hasattr(models.Diploma, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Diploma, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Diploma, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.DiplomaResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )



    @classmethod
    def get_multi(
        cls,
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None,
    ):
        
        if page < 1:
            page = 1

        record_query = db.query(models.Candidat)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Candidat.first_name.ilike(f'%{keyword}%'),
                    models.Candidat.last_name.ilike(f'%{keyword}%'),
                    models.Candidat.email.ilike(f'%{keyword}%'),
                    models.Candidat.phone_number.ilike(f'%{keyword}%'),
                    models.Candidat.civility.ilike(f'%{keyword}%'),
                )
            )

        if order and order_field and hasattr(models.Candidat, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Candidat, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Candidat, order_field).desc())
        
        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CandidateResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


    @classmethod
    def get_all_candidates(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
    ):

        if page < 1:
            page = 1

        record_query = db.query(models.Candidat).filter(models.Candidat.is_deleted==False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Candidat.first_name.ilike(f'%{keyword}%'),
                    models.Candidat.last_name.ilike(f'%{keyword}%'),
                    models.Candidat.email.ilike(f'%{keyword}%'),
                    models.Candidat.phone_number.ilike(f'%{keyword}%'),
                    models.Candidat.civility.ilike(f'%{keyword}%'),
                )
            )

        if order and order_field and hasattr(models.Candidat, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Candidat, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Candidat, order_field).desc())

        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.AllCandidateResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )






candidate = CRUDCandidat(models.Candidat)