from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/competences", tags=["competences"])

@router.post("/create",response_model=schemas.Msg)
async def create_competences(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.CompetenceCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.competences.create(
        db=db,
        obj_in=obj_in,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="competence-created-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_competence(
    *,
    db: Session = Depends(get_db),
    competence:schemas.CompetenceUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.competences.update(
        db=db,
        competence=competence,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="competence-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_competence(
    *,
    db: Session = Depends(get_db),
    competence:schemas.CompetenceDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.competences.delete(db=db,competence=competence,uuid=competence.uuid)
    return schemas.Msg(message=__(key="competence-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_competence(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.CompetenceDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.competences.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="competence-deleted-successfully"))




@router.get("/get-my-competences", response_model=None)
async def get_all_my_competences(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.competences.get_my_competences(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )