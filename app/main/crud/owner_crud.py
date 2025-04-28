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


class CRUDOwner(CRUDBase[models.Owner,schemas.OwnerCreate,schemas.OwnerSchemaUpdate]):

    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Owner).filter(models.Owner.email==email,models.Owner.is_deleted==False).first()
    
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Owner).filter(models.Owner.uuid==uuid,models.Owner.is_deleted==False).first()
    

    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Owner).filter(models.Owner.phone_number==phone_number,models.Owner.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.OwnerCreate,added_by:str):
        password :str = generate_password(8,8)
        print(f"User password {password}")
        common_uuid = str(uuid.uuid4())
        db_obj = models.Owner(
            uuid = common_uuid,
            firstname = obj_in.firstname,
            lastname = obj_in.lastname,
            email = obj_in.email,
            avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else None,
            password_hash = get_password_hash(password),
            added_by=added_by,
            status = models.Ownerstatus.UNACTIVED

        )
        db.add()
        db.commit()
        db.refresh(db_obj)

        new_user = models.User(
            uuid = common_uuid,
            email = obj_in.email,
            first_name = obj_in.firstname,
            last_name = obj_in.lastname,
            phone_number = obj_in.phone_number,
            role = models.UserRole.OWNER,
            password_hash = get_password_hash(password),
        )
        db.add()
        db.commit()
        db.refresh(new_user)
        return db_obj
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.OwnerSchemaUpdate,added_by:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="owner-not-found"))
        db_obj.firstname = obj_in.firstname if obj_in.firstname else db_obj.firstname
        db_obj.lastname = obj_in.lastname if obj_in.lastname else db_obj.lastname
        db_obj.email = obj_in.email if obj_in.email else db_obj.email
        db_obj.phone_number = obj_in.phone_number if obj_in.phone_number else db_obj.phone_number
        db_obj.avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else db_obj.avatar_uuid
        added_by=added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="owner-not-found"))
        db_obj.is_deleted==True
        db.commit()

    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="owner-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def update_status(cls,db:Session,uuid:str,status:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404,detail=__(key="owner-not-found"))
        db_obj.status = status
        db.commit()
    

    @classmethod
    def get_many(
        cls,
        db:Session,
        page:int = 1,
        per_page:int = 30,
        order:Optional[str] = None,
        status:Optional[str] = None,
        keyword:Optional[str]= None
    ):
        record_query = db.query(models.Owner).filter(models.Owner.status.not_in([models.Ownerstatus.BLOCKED,models.Ownerstatus.DELETED]))
        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Owner.firstname.ilike('%' + str(keyword) + '%'),
                    models.Owner.email.ilike('%' + str(keyword) + '%'),
                    models.Owner.lastname.ilike('%' + str(keyword) + '%'),
                    models.Owner.phone_number.ilike('%' + str(keyword) + '%'),

                )
            )
        if status:
            record_query = record_query.filter(models.Owner.status == status)
        
        if order and order.lower() == "asc":
            record_query = record_query.order_by(models.Owner.date_added.asc())
        
        elif order and order.lower() == "desc":
            record_query = record_query.order_by(models.Owner.date_added.desc())
        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page)

        return schemas.OwnerResponseList(
            total = total,
            pages = math.ceil(total/per_page),
            per_page = per_page,
            current_page =page,
            data =record_query
        )




