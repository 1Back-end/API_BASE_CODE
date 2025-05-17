from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/offers", tags=["offers"])

@router.post("/create",response_model=schemas.Msg)
def create_offers(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.JobOffersCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"])),  
):
    crud.offers.create(db=db,obj_in=obj_in,background_tasks=background_tasks,added_by=current_user.uuid)
    return schemas.Msg(message=__(key="offer-created-successfully"))

@router.put("/update",response_model=schemas.Msg)
def update_offers(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.JobOffersUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    offer = crud.offers.get_by_uuid(db=db,uuid=obj_in.uuid)
    if not offer:
            raise HTTPException(status_code=404,detail=__(key="offer-not-found"))
    if offer.added_by != current_user.uuid:
        raise HTTPException(status_code=403, detail=__("not-authorized"))
    crud.offers.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return schemas.Msg(message=__(key="offer-updated-successfully"))

@router.put("/update-status",response_model=schemas.Msg)
def update_status_offers(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.JobOffersUpdateStatus,
    status: str = Query(..., enum=[st.value for st in models.JobStatus]),
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    offers = crud.offers.get_by_uuid(db=db,uuid=obj_in.uuid)
    if not offers:
            raise HTTPException(status_code=404,detail=__(key="offers-not-found"))
    if offers.added_by != current_user.uuid:
        raise HTTPException(status_code=403, detail=__("not-authorized"))
    crud.offers.update_status(db=db,uuid=obj_in.uuid,status=status)
    return schemas.Msg(message=__(key="offer-status-updated-successfully"))

@router.put("/delete",response_model=schemas.Msg)
def delete_offers(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.JobOffersDelete,
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    offers = crud.offers.get_by_uuid(db=db,uuid=obj_in.uuid)
    if not offers:
            raise HTTPException(status_code=404,detail=__(key="offers-not-found"))
    if offers.added_by != current_user.uuid:
        raise HTTPException(status_code=403, detail=__("not-authorized"))
    crud.offers.delete(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="offer-deleted-successfully"))

@router.get("/get_many_owners", response_model=None)
async def get_owners_offers(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    status: str = Query(..., enum=[st.value for st in models.JobStatus]),
    work_mode: str = Query(..., enum=[st.value for st in models.WorkMode]),
    employment_type: str = Query(..., enum=[st.value for st in models.ContractType]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    return crud.offers.get_multi_owners(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        work_mode=work_mode,
        employment_type=employment_type,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        added_by=current_user.uuid
        
    )


@router.get("/get_many", response_model=None)
async def get_many_offers(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    status: str = Query(..., enum=[st.value for st in models.JobStatus]),
    work_mode: str = Query(..., enum=[st.value for st in models.WorkMode]),
    employment_type: str = Query(..., enum=[st.value for st in models.ContractType]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
):
    return crud.offers.get_many(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        work_mode=work_mode,
        employment_type=employment_type,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword
        
    )



