import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas

class CRUDMedia(CRUDBase[models.Media, schemas.MediaCreate, schemas.MediaUpdate]):

    @classmethod
    def get_by_uuid(cls, db: Session, uuid: str):
        return db.query(models.Media).filter(models.Media.uuid == uuid, models.Media.is_deleted == False).first()

    @classmethod
    def get_by_candidate_uuid(cls, db: Session, candidate_uuid: str):
        return db.query(models.Media).filter(models.Media.candidate_uuid == candidate_uuid, models.Media.is_deleted == False).first()

    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.MediaCreate, candidate_uuid: str):
        new_media = models.Media(
            uuid = str(uuid.uuid4()),
            title = obj_in.title,
            link = obj_in.link,
            candidate_uuid = candidate_uuid
        )
        db.add(new_media)
        db.commit()
        db.refresh(new_media)
        return new_media

    @classmethod
    def update(cls,db:Session,*,media:schemas.MediaUpdate,candidate_uuid:str):
        db_obj = cls.get_by_uuid(db,uuid=media.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key=" social media-info-not-found"))

        db_obj.title = media.title if media.title else db_obj.title
        db_obj.link = media.link if media.link else db_obj.link
        db_obj.candidate_uuid = candidate_uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj




    @classmethod
    def get_my_medias(
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


        record_query = db.query(models.Media).filter(models.Media.is_deleted == False,models.Media.candidate_uuid == candidate_uuid)
        if keyword:

                record_query = record_query.filter(
                    or_(
                        models.Media.title.ilike(f'%{keyword}%'),
                    )
                )
    
            

        if order and order_field and hasattr(models.Media, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Media, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Media, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.MediaResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

   
    @classmethod
    def delete(cls, db: Session, uuid:str):
        media = cls.get_by_uuid(db=db,uuid=uuid)
        if not media:
            raise HTTPException(status_code=404,detail=__(key="social-media-not-found"))
        db.delete(media)
        db.commit()

    @classmethod
    def soft_delete(cls,db:Session,*,uuid:str):
        media = cls.get_by_uuid(db=db, uuid=uuid)
        if not media:
            raise HTTPException(status_code=404, detail=__("social-media-not-found"))
        media.is_deleted = True
        db.commit()



medias = CRUDMedia(models.Media)