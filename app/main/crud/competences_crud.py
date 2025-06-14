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




class CRUDCompetence(CRUDBase[models.Competence,schemas.CompetenceCreate,schemas.CompetenceUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Competence).filter(models.Competence.uuid==uuid,models.Competence.is_deleted==False).first()
    @classmethod
    def get_by_candidate_uuid(cls,db:Session,*,candidate_uuid:str):
        return db.query(models.Competence).filter(models.Competence.candidate_uuid==candidate_uuid,models.Competence.is_deleted==False).all()
    
    @classmethod
    def create(cls, db: Session, *, competence: schemas.CompetenceCreate,candidate_uuid:str):
        
        new_competence = models.Competence(
            uuid = str(uuid.uuid4()),
            title = competence.title,
            level = competence.level,
            is_certified = competence.is_certified,
            description=competence.description,
            candidate_uuid = candidate_uuid
            
        )
        db.add(new_competence)
        db.commit()
        db.refresh(new_competence)
        return new_competence
    

    @classmethod
    def update(cls,db:Session,*,competence:schemas.CompetenceUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=competence.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="competence-not-found"))

        db_obj.title = competence.title if competence.title else db_obj.title
        db_obj.level = competence.level if competence.level else db_obj.level
        db_obj.is_certified = competence.is_certified if competence.is_certified else db_obj.is_certified
        db_obj.description = competence.description if competence.description else db_obj.description
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_my_competences(
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


        record_query = db.query(models.Competence).filter(models.Competence,models.Competence.is_deleted == False)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Competence.title.ilike(f'%{keyword}%'),
                        models.Competence.level.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.Competence, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Competence, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Competence, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CompetenceResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

   
    @classmethod
    def delete(cls, db: Session, uuid:str):
        competence = cls.get_by_uuid(db=db,uuid=uuid)
        if not competence:
            raise HTTPException(status_code=404,detail=__(key="competence-not-found"))
        competence.is_deleted = True
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,*,uuid:str):
        competence = cls.get_by_uuid(db=db, uuid=uuid)
        if not competence:
            raise HTTPException(status_code=404, detail=__("competence-not-found"))
        competence.is_deleted = True
        db.commit()


competences = CRUDCompetence(models.Competence)