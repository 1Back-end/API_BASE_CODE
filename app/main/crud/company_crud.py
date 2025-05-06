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
from app.main import models,schemas,crud

class CRUDCompany(CRUDBase[models.Company,schemas.CompanyCreate,schemas.CompanyUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Company).filter(models.Company.uuid==uuid,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_type(cls,db:Session,*,type:str):
        return db.query(models.Company).filter(models.Company.type==type,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Company).filter(models.Company.email==email,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_owner_uuid(cls,db:Session,*,owner_uuid:str):
        return db.query(models.Company).filter(models.Company.added_by==owner_uuid,models.Company.is_deleted==False).all()

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.CompanyCreate,added_by:str):
        if obj_in.logo_uuid:
            logo = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.logo_uuid)
            if not logo:
                raise HTTPException(status_code=404, detail=__("logo-not-found"))

        if obj_in.signature_uuid:
            signature = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.signature_uuid)
            if not signature:
                raise HTTPException(status_code=404, detail=__("signature-not-found"))

        if obj_in.stamp_uuid:
            stamp = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.stamp_uuid)
            if not stamp:
                raise HTTPException(status_code=404, detail=__("stamp-not-found"))
        address = crud.address.get_by_uuid(db=db, uuid=obj_in.address_uuid)
        if not address:
            raise HTTPException(status_code=404, detail=__(key="address-not-found"))
        
        company = models.Company(
           uuid=str(uuid.uuid4()),
           name=obj_in.name,
           email=obj_in.email,
           phone=obj_in.phone,
           description=obj_in.description,
           slogan=obj_in.slogan,
           address_uuid=obj_in.address_uuid,
           logo_uuid=obj_in.logo_uuid if obj_in.logo_uuid else None,
           signature_uuid=obj_in.signature_uuid if obj_in.signature_uuid else None,
           stamp_uuid=obj_in.stamp_uuid if obj_in.stamp_uuid else None,
           founded_at=obj_in.founded_at,
           employee_count=obj_in.employee_count,
           added_by=added_by,
           website=obj_in.website
           
       )
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    
    @classmethod
    def update(cls, db: Session, *, obj_in: schemas.CompanyUpdate,added_by:str):
        if obj_in.logo_uuid:
            logo = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.logo_uuid)
            if not logo:
                raise HTTPException(status_code=404, detail=__("logo-not-found"))

        if obj_in.signature_uuid:
            signature = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.signature_uuid)
            if not signature:
                raise HTTPException(status_code=404, detail=__("signature-not-found"))

        if obj_in.stamp_uuid:
            stamp = crud.storage_crud.get_file_by_uuid(db=db, file_uuid=obj_in.stamp_uuid)
            if not stamp:
                raise HTTPException(status_code=404, detail=__("stamp-not-found"))
        address = crud.address.get_by_uuid(db=db, uuid=obj_in.address_uuid)
        if not address:
            raise HTTPException(status_code=404, detail=__(key="address-not-found"))
        company = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not company:
            raise HTTPException(status_code=404, detail=__("company-not-found"))
        company.name = obj_in.name if obj_in.name else company.name
        company.email = obj_in.email if obj_in.email else company.email
        company.phone = obj_in.phone if obj_in.phone else company.phone
        company.description = obj_in.description if obj_in.description else company.description
        company.slogan = obj_in.slogan if obj_in.slogan else company.slogan
        company.address_uuid = obj_in.address_uuid if obj_in.address_uuid else company.address_uuid
        company.logo_uuid = obj_in.logo_uuid if obj_in.logo_uuid else company.logo_uuid
        company.signature_uuid = obj_in.signature_uuid if obj_in.signature_uuid else company.signature_uuid
        company.stamp_uuid = obj_in.stamp_uuid if obj_in.stamp_uuid else company.stamp_uuid
        company.founded_at = obj_in.founded_at if obj_in.founded_at else company.founded_at
        company.employee_count = obj_in.employee_count if obj_in.employee_count else company.employee_count
        company.website = obj_in.website if obj_in.website else company.website
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    


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
        status: Optional[str] = None,
        type:Optional[str] = None,
        owner_uuid: str = None
    ):
        
        if page < 1:
            page = 1

        record_query = db.query(models.Company).filter(models.Company.added_by == owner_uuid)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Company.name.ilike(f'%{keyword}%'),
                    models.Company.phone.ilike(f'%{keyword}%'),
                    models.Company.email.ilike(f'%{keyword}%'),
                    models.Company.slogan.ilike(f'%{keyword}%'),
                    models.Company.description.ilike(f'%{keyword}%'),
                    models.Company.website.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Company, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Company, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Company, order_field).desc())
        if status:
            record_query = record_query.filter(models.Company.status == status)
        if type:
            record_query = record_query.filter(models.Company.type == type)


        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CompanyResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        company = cls.get_by_uuid(db=db, uuid=uuid)
        if not company:
            raise HTTPException(status_code=404, detail=__("company-not-found"))
        company.is_deleted = True
        db.commit()
    
    @classmethod
    def update_status(cls,db:Session,*,status:str,uuid:str):
        company = cls.get_by_uuid(db=db, uuid=uuid)
        if not company:
            raise HTTPException(status_code=404, detail=__("company-not-found"))
        company.status = status
        db.commit()


    @classmethod
    def get_multi_admin(
        cls,
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        type:Optional[str] = None,
        owner_uuid: str = None
    ):
        
        if page < 1:
            page = 1

        record_query = db.query(models.Company).filter(models.Company.is_deleted==False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Company.name.ilike(f'%{keyword}%'),
                    models.Company.phone.ilike(f'%{keyword}%'),
                    models.Company.email.ilike(f'%{keyword}%'),
                    models.Company.slogan.ilike(f'%{keyword}%'),
                    models.Company.description.ilike(f'%{keyword}%'),
                    models.Company.website.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Company, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Company, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Company, order_field).desc())
        if status:
            record_query = record_query.filter(models.Company.status == status)
        if type:
            record_query = record_query.filter(models.Company.type == type)
        if owner_uuid:
            record_query = record_query.filter(models.Company.added_by == owner_uuid)


        total = record_query.count()

        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CompanyResponseListSlim1(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )


            
    
    
        
    
company = CRUDCompany(models.Company)