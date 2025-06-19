import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import Optional
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas




class CRUDStrength(CRUDBase[models.Strength,schemas.StrengthCreate,schemas.StrengthUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Strength).filter(models.Strength.uuid==uuid,models.Strength.is_deleted==False).first()
    @classmethod
    def get_by_candidate_uuid(cls,db:Session,*,candidate_uuid:str):
        return db.query(models.Strength).filter(models.Strength.candidate_uuid==candidate_uuid,models.Strength.is_deleted==False).all()
    
    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.StrengthCreate,candidate_uuid:str):
        
        new_strength = models.Strength(
            uuid = str(uuid.uuid4()),
            title = obj_in.title,
            level = obj_in.level,
            description=obj_in.description,
            candidate_uuid = candidate_uuid
            
        )
        db.add(new_strength)
        db.commit()
        db.refresh(new_strength)
        return new_strength
    

    @classmethod
    def update(cls,db:Session,*,strength:schemas.StrengthUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=strength.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="strength-not-found"))

        db_obj.title = strength.title if strength.title else db_obj.title
        db_obj.level = strength.level if strength.level else db_obj.level
        db_obj.description = strength.description if strength.description else db_obj.description
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj



    @classmethod
    def get_my_strengths(
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


        record_query = db.query(models.Strength).filter(models.Strength.is_deleted == False,models.Strength.candidate_uuid == candidate_uuid)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Strength.title.ilike(f'%{keyword}%'),
                        models.Strength.description.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.Strength, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Strength, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Strength, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.StrengthResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

   
    @classmethod
    def delete(cls, db: Session, uuid:str):
        strength = cls.get_by_uuid(db=db,uuid=uuid)
        if not strength:
            raise HTTPException(status_code=404,detail=__(key="strength-not-found"))
        db.delete(strength)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,*,uuid:str):
        strength = cls.get_by_uuid(db=db, uuid=uuid)
        if not strength:
            raise HTTPException(status_code=404, detail=__("strength-not-found"))
        strength.is_deleted = True
        db.commit()



strengths = CRUDStrength(models.Strength)