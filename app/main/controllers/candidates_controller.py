from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash,is_valid_password
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/candidate", tags=["candidate"])

@router.post("/create", response_model=schemas.Msg)
def create_candidate(
    candidate: schemas.CandidateCreate, 
    db: Session = Depends(get_db)
):
    exist_email = crud.candidate.get_by_email(db=db,email=candidate.email)
    if exist_email:
        raise HTTPException(status_code=404, detail=__(key="candidat-email-already-exist"))
    
    exist_phone_number = crud.candidate.get_by_phone_number(db=db,phone_number=candidate.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=404, detail=__(key="candidat-phone-number-already-exist"))
    exist_user_phone = crud.user.get_by_phone_number(db=db, phone_number=candidate.phone_number)
    if exist_user_phone:
        raise HTTPException(status_code=409, detail=__(key="user-phone-number-already-used"))

    exist_user_email = crud.user.get_by_email(db=db, email=candidate.email)
    if exist_user_email:
        raise HTTPException(status_code=409, detail=__(key="user-email-already-used"))

    if not is_valid_password(candidate.password):
        raise HTTPException(status_code=400, detail=__(key="invalid-password"))

    # Appel au CRUD pour créer un candidat et ses expériences
    crud.candidate.create(db=db,candidate=candidate)
    return {"message": __(key="candidate-created")}


@router.post("/create-diplomas",response_model=schemas.Msg)
async def create_my_diplomas(
        diploma: schemas.DiplomaCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.candidate.create_diplomas(
        db=db,
        diploma=diploma,
        candidate_uuid=current_user.uuid,
    )
    return {"message": __(key="diplomas-created")}

@router.put("/update-diplomas", response_model=schemas.Msg)
async def update_my_diplomas(
        obj_in: schemas.DiplomaUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):

    crud.candidate.update_diplomas(
        db=db,
        obj_in=obj_in,
        candidate_uuid=current_user.uuid,
    )
    return {"message": __(key="diplomas-updated")}


@router.get("/get_diplomas_by_uuid",response_model=schemas.DiplomasBase)
async def get_diplomas_by_uuid(
        uuid: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    data = crud.candidate.get_diploma_by_uuid(db=db,uuid=uuid)
    return data


@router.put("/delete-diplomas",response_model=schemas.Msg)
async def delete_diplomas(
        obj_in: schemas.DiplomaDelete,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.candidate.delete_diplomas(db=db,uuid=obj_in.uuid)
    return {"message": __(key="diplomas-deleted")}


@router.get("/get-my-diplomas", response_model=None)
async def get_all_my_diplomas(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.candidate.get_my_diplomas(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )







@router.post("/create-my-experiences", response_model=schemas.Msg)
async def create_my_experiences(
        *,
        experiences:schemas.ExperenciesCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.candidate.create_experiences(
        db=db,
        experiences=experiences,
        candidate_uuid=current_user.uuid,
    )
    return {"message": __(key="experiences-created")}

@router.put("/delete-experiences",response_model=schemas.Msg)
async def delete_diplomas(
        obj_in: schemas.DiplomaExperience,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.candidate.delete_experiences(db=db,uuid=obj_in.uuid)
    return {"message": __(key="experiences-deleted")}



@router.put("/update-my-experiences", response_model=None)
async def update_my_experiences(
        *,
        experiences:schemas.ExperenciesUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):

    crud.candidate.update_experiences(
        db=db,
        experiences=experiences,
        candidate_uuid=current_user.uuid,
    )


@router.get("/get-my-experiences", response_model=None)
async def get_all_my_experiences(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.candidate.get_my_experiences(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )

@router.get("/get-experiences-by-uuid",response_model=schemas.ExperenciesBase)
async def get_experiences_by_uuid(
        uuid: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    data = crud.candidate.get_my_experiences_by_uuid(db=db,uuid=uuid)
    return data



@router.get("/get_many", response_model=None)
async def get_many_candidate(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
):
    return crud.candidate.get_multi(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,

    )



@router.get("/get_all_candidates-for_website", response_model=None)
async def get_many_candidate_for_website(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order: str = Query(None, enum=["ASC", "DESC"]),
    keyword: Optional[str] = None,
    order_field: Optional[str] = None,  # Correction de order_filed → order_field
):
    return crud.candidate.get_all_candidates(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,

    )