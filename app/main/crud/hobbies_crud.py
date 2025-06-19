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




class CRUDHobby(CRUDBase[models.Hobby,schemas.HobbyCreate,schemas.HobbyUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Hobby).filter(models.Hobby.uuid==uuid,models.Hobby.is_deleted==False).first()
    @classmethod
    def get_by_candidate_uuid(cls,db:Session,*,candidate_uuid:str):
        return db.query(models.Hobby).filter(models.Hobby.candidate_uuid==candidate_uuid,models.Hobby.is_deleted==False).all()
    
    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.HobbyCreate,candidate_uuid:str):
        
        new_hobby = models.Hobby(
            uuid = str(uuid.uuid4()),
            title = obj_in.title,
            description=obj_in.description,
            candidate_uuid = candidate_uuid
            
        )
        db.add(new_hobby)
        db.commit()
        db.refresh(new_hobby)
        return new_hobby
    

    @classmethod
    def update(cls,db:Session,*,hobby:schemas.HobbyUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=hobby.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="hobby-not-found"))

        db_obj.title = hobby.title if hobby.title else db_obj.title
        db_obj.description = hobby.description if hobby.description else db_obj.description
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj



    @classmethod
    def get_my_hobbies(
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


        record_query = db.query(models.Hobby).filter(models.Hobby.is_deleted == False,models.Hobby.candidate_uuid == candidate_uuid)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Hobby.title.ilike(f'%{keyword}%'),
                        models.Hobby.description.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.Hobby, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Hobby, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Hobby, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.HobbyResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

   
    @classmethod
    def delete(cls, db: Session, uuid:str):
        hobby = cls.get_by_uuid(db=db,uuid=uuid)
        if not hobby:
            raise HTTPException(status_code=404,detail=__(key="hobby-not-found"))
        db.delete(hobby)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,*,uuid:str):
        hobby = cls.get_by_uuid(db=db, uuid=uuid)
        if not hobby:
            raise HTTPException(status_code=404, detail=__("hobby-not-found"))
        hobby.is_deleted = True
        db.commit()



hobbies = CRUDHobby(models.Hobby)