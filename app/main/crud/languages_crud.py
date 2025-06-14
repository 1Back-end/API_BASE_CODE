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




class CRUDLanguage(CRUDBase[models.Language,schemas.LanguageCreate,schemas.LanguageUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Language).filter(models.Language.uuid==uuid,models.Language.is_deleted==False).first()
    @classmethod
    def get_by_candidate_uuid(cls,db:Session,*,candidate_uuid:str):
        return db.query(models.Language).filter(models.Language.candidate_uuid==candidate_uuid,models.Language.is_deleted==False).all()
    
    @classmethod
    def create(cls, db: Session, *, Language: schemas.LanguageCreate,candidate_uuid:str):
        
        new_competence = models.Language(
            uuid = str(uuid.uuid4()),
            title = language.title,
            level = language.level,
            description=language.description,
            candidate_uuid = candidate_uuid
            
        )
        db.add(new_language)
        db.commit()
        db.refresh(new_language)
        return new_language
    

    @classmethod
    def update(cls,db:Session,*,language:schemas.LanguageUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=language.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="language-not-found"))

        db_obj.title = language.title if language.title else db_obj.title
        db_obj.level = language.level if language.level else db_obj.level
        db_obj.description = language.description if language.description else db_obj.description
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_my_languages(
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


        record_query = db.query(models.Language).filter(models.Language,models.Competence.is_deleted == False)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Competence.title.ilike(f'%{keyword}%'),
                        models.Competence.level.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.languages, order_field):
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


competences = CRUDcompetence(models.Competence)