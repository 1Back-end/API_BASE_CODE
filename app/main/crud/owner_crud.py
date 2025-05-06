from datetime import datetime, timedelta
import math
from typing import Union, Optional, List
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import or_
from app.main.core.i18n import __, get_language
from app.main.core.mail import send_account_owner_creation
from app.main.crud.base import CRUDBase
from sqlalchemy.orm import Session,joinedload
from app.main import schemas, models,crud
import uuid
from app.main.core.security import get_password_hash, verify_password, generate_password


class CRUDOwner(CRUDBase[models.Owner, schemas.OwnerCreate,schemas.OwnerUpdate]):

    @classmethod
    def get_by_email(cls, db: Session, *, email: EmailStr) -> Optional[models.Owner]:
        return db.query(models.Owner).filter(models.Owner.email == email).first()
    
    @classmethod
    def get_by_uuid(cls, db: Session, *, uuid:str):
        return db.query(models.Owner).filter(models.Owner.uuid == uuid).first()
    
    @classmethod
    def create(cls, db: Session, *, obj_in: schemas.OwnerCreate,added_by_uuid:str):
        password: str = generate_password(8, 8)
        print(f"Owner password: {password}")
        owner = models.Owner(
            uuid= str(uuid.uuid4()),
            email = obj_in.email,
            full_phone_number=f"{obj_in.country_code}{obj_in.phone_number}",
            country_code=obj_in.country_code,
            phone_number=obj_in.phone_number,
            firstname = obj_in.firstname,
            lastname = obj_in.lastname,
            password_hash = get_password_hash(password),
            avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else None,
            added_by_uuid = added_by_uuid,
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        send_account_owner_creation(email_to=obj_in.email,firstname=obj_in.firstname,
                                    password=password)
        return owner
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.OwnerUpdate,added_by_uuid:str):
        owner = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if owner is None:
            raise HTTPException(status_code=404,detail=__(key="owner-not-found"))
        owner.email = obj_in.email if obj_in.email else owner.email
        owner.firstname = obj_in.firstname if obj_in.firstname else owner.firstname
        owner.lastname = obj_in.lastname if obj_in.lastname else owner.lastname
        owner.avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else owner.avatar_uuid
        owner.phone_number = obj_in.phone_number if obj_in.phone_number else owner.phone_number
        owner.country_code = obj_in.country_code if obj_in.country_code else owner.country_code
        db.flush()
        db.commit()
        db.refresh(owner)
        return owner
    

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
    @classmethod
    def update_status(cls, db: Session, uuid:str,status:str) -> models.Owner:
        owner = cls.get_by_uuid(db=db,uuid=uuid)
        if not owner:
         raise HTTPException(status_code=404, detail=__("owner-not-found"))
        owner.status = status
        db.commit()
        return owner
    @classmethod
    def soft_delete(cls,db:Session,uuid:str):
        owner = cls.get_by_uuid(db=db,uuid=uuid)
        if not owner:
         raise HTTPException(status_code=404, detail=__("owner-not-found"))
        owner.status =  models.Ownerstatus.DELETED
        db.commit()

    @classmethod
    def authenticate(cls, db: Session, *, email: str, password: str) -> Optional[models.Owner]:
        db_obj: models.Owner = db.query(models.Owner).filter(models.Owner.email == email).first()
        if not db_obj:
            return None
        if not verify_password(password, db_obj.password_hash):
            return None
        return db_obj
    
    def is_active(self, owner: models.Owner) -> bool:
        return owner.status == models.Ownerstatus.ACTIVED

        

  
owner = CRUDOwner(models.Owner)


