from datetime import timedelta, datetime
import math
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import CandidateTokenRequired

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/create",response_model=schemas.Msg)
def applied_offers(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ApplicationCreate,
    current_user: models.Candidat = Depends(CandidateTokenRequired())
):
    candidate_uuid = current_user.uuid
    crud.application.create(db=db,obj_in=obj_in,candidate_uuid=candidate_uuid)
    return schemas.Msg(message=__(key="offer-applied-successfully"))

@router.put("/update-_status-application",response_model=schemas.Msg)
def update_status_application(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ApplicationDetails,
    status: str = Query(..., enum=[st.value for st in models.ApplicationStatusEnum]),
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    crud.application.update_status(db=db,uuid=obj_in.uuid,status=status)
    return schemas.Msg(message=__(key="application-status-update-successfully"))

@router.put("/delete-application",response_model=schemas.Msg)
def delete_application(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.ApplicationDetails,
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"]))
):
    crud.application.delete(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="application-delete-successfully"))

@router.get("/get_many-application", response_model=None)
async def get_many_application(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    status: str = Query(..., enum=[st.value for st in models.ApplicationStatusEnum]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    return crud.application.get_multi(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        
    )



@router.get("/candidates/by-offer", response_model=schemas.ApplicationResponseList)
def get_applications_by_offer(
    job_offer_uuid: str = Query(..., description="UUID de l'offre d'emploi"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["OWNER"])),
    page: int = 1,
    per_page: int = 30
):
    # Vérifie que l'offre appartient à l'utilisateur connecté
    job_offer = db.query(models.JobOffer).filter(
        models.JobOffer.uuid == job_offer_uuid,
        models.JobOffer.added_by == current_user.uuid,
        models.JobOffer.is_deleted == False
    ).first()

    if not job_offer:
        raise HTTPException(status_code=403, detail=__(key="offer-not-found"))

    # Récupère les candidatures liées à cette offre
    record_query = db.query(models.Application).filter(
        models.Application.job_offer_uuid == job_offer_uuid,
        models.Application.is_deleted == False
    )

    total = record_query.count()
    records = record_query.offset((page - 1) * per_page).limit(per_page).all()

    return schemas.ApplicationResponseListSlim(
        total=total,
        pages=math.ceil(total / per_page),
        per_page=per_page,
        current_page=page,
        data=records
    )