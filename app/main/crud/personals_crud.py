import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas

class CRUDPersonal(CRUDBase[models.Personal, schemas.PersonalCreate, schemas.PersonalUpdate]):

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str):
        return db.query(models.Personal).filter(models.Personal.uuid == uuid, models.Personal.is_deleted == False).first()

    @classmethod
    def get_by_candidat_uuid(cls, db: Session, candidat_uuid: str):
        return db.query(models.Personal).filter(models.Personal.candidate_uuid == candidat_uuid,models.Personal.is_deleted == False).first()

    @classmethod
    def get_by_candidate_uuid(cls, db: Session, candidate_uuid: str):
        return db.query(models.Personal).filter(models.Personal.candidate_uuid == candidate_uuid, models.Personal.is_deleted == False).first()

    @classmethod
    def create_or_update(cls, db: Session, *, obj_in: schemas.PersonalCreate, candidate_uuid: str):
        existing = db.query(models.Personal).filter_by(candidate_uuid=candidate_uuid).first()

        if existing:
            for field, value in obj_in.dict().items():
                setattr(existing, field, value)
            db.commit()
            db.refresh(existing)
            return existing
        else:
            new_personal = models.Personal(
                uuid=str(uuid.uuid4()),
                candidate_uuid=candidate_uuid,
                **obj_in.dict()
            )
            db.add(new_personal)
            db.commit()
            db.refresh(new_personal)
            return new_personal


    @classmethod
    def update(cls,db:Session,*,personal:schemas.PersonalUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=personal.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="personal-info-not-found"))

        db_obj.gender = personal.gender if personal.gender else db_obj.gender
        db_obj.professional_title = personal.professional_title if personal.professional_title else db_obj.professional_title
        db_obj.title_description = personal.title_description if personal.title_description else db_obj.title_description
        db_obj.birth_date = personal.birth_date if personal.birth_date else db_obj.birth_date
        db_obj.place_of_birth = personal.place_of_birth if personal.place_of_birth else db_obj.place_of_birth
        db_obj.region_of_origin = personal.region_of_origin if personal.region_of_origin else db_obj.region_of_origin
        db_obj.adress = personal.adress if personal.adress else db_obj.adress
        db_obj.nationality = personal.nationality if personal.nationality else db_obj.nationality
        db_obj.city = personal.city if personal.city else db_obj.city
        db_obj.country = personal.country if personal.country else db_obj.country
        db_obj.others = personal.others if personal.others else db_obj.others
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj




    @classmethod
    def get_my_personals(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,
            candidate_uuid: Optional[str] = None
            
    ):
        if page < 1:
            page = 1


        record_query = db.query(models.Personal).filter(models.Personal.is_deleted == False,models.Personal.candidate_uuid == candidate_uuid)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Personal.professional_title.ilike(f'%{keyword}%'),
                        models.Personal.city.ilike(f'%{keyword}%'),
                        models.Personal.region_of_origin.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.Personal, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Personal, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Personal, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.PersonalResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

   
    @classmethod
    def delete(cls, db: Session, uuid:str):
        personal = cls.get_by_uuid(db=db,uuid=uuid)
        if not personal:
            raise HTTPException(status_code=404,detail=__(key="personal-info-not-found"))
        db.delete(personal)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,*,uuid:str):
        personal = cls.get_by_uuid(db=db, uuid=uuid)
        if not personal:
            raise HTTPException(status_code=404, detail=__("personal-info-not-found"))
        personal.is_deleted = True
        db.commit()



personals = CRUDPersonal(models.Personal)