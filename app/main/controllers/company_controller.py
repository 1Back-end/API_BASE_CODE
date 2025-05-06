from datetime import timedelta, datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
# from app.main.core.dependencies import OwnerTokenRequired

router = APIRouter(prefix="/company", tags=["company"])

@router.post("/create/owners", response_model=schemas.CompanyResponse)
async def create_company(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CompanyCreate,
     current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
):
    exist_email = crud.company.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail=__(key="this-email-is-already-in-used"))
    added_by=current_user.uuid
    return crud.company.create(db=db,obj_in=obj_in,added_by=added_by)

@router.put("/update/owners",response_model=schemas.CompanyResponse)
async def update_company(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.CompanyUpdate,
     current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
):
    exist_email = crud.company.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail=__(key="this-email-is-already-in-used"))
    company = crud.company.get_by_uuid(db=db, uuid=obj_in.uuid)
    if not company:
        raise HTTPException(status_code=404, detail=__("company-not-found"))
    # Vérifier si l'utilisateur est bien le propriétaire de l'entreprise
    if company.added_by != current_user.uuid:
        raise HTTPException(status_code=403, detail=__("not-authorized"))
    return crud.company.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    

@router.get("/get_many/owners", response_model=None)
async def get_many_company(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    status: str = Query(..., enum=[st.value for st in models.CompanyStatus]),
    type: str = Query(..., enum=[st.value for st in models.CompanyType]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
     current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
):
    return crud.company.get_multi(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        type=type,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        owner_uuid=current_user.uuid  # Ajout du filtre par propriétaire
    )

@router.delete("/delete/auth",response_model=schemas.Msg)
async def delete_company(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CompanyDelete,
    current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
    
):
    crud.company.delete(db=db, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="company-deleted-successfully"))

@router.put("/update_status/auth",response_model=schemas.Msg)
async def update_status_company(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CompanyUpdateStatus,
    status: str = Query(..., enum=[st.value for st in models.CompanyStatus]), 
    current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
):
    crud.company.update_status(db=db, status=status, uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="company-status-updated-successfully"))

@router.get("/get_owner_company/auth",response_model=List[schemas.CompanyResponse])
async def get_owner_company(
    *,
    db: Session = Depends(get_db),
    owner_uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["Owner"]))

):
    return crud.company.get_by_owner_uuid(db=db,owner_uuid=owner_uuid)

@router.get("/get_many/auth", response_model=None)
async def get_many_company_by_admin(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    status: str = Query(..., enum=[st.value for st in models.CompanyStatus]),
    type: str = Query(..., enum=[st.value for st in models.CompanyType]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
    owner_uuid:Optional[str] = None,
    current_user: models.User = Depends(TokenRequired(roles=["Owner"]))
):
    return crud.company.get_multi_admin(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        type=type,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        owner_uuid=owner_uuid  # Ajout du filtre par propriétaire
    )