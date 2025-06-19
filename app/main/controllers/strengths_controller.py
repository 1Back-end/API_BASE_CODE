from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/strengths", tags=["strengths"])

@router.post("/create",response_model=schemas.Msg)
async def create_strength(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.StrengthCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.strengths.create(
        db=db,
        obj_in=obj_in,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="strength-created-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_strength(
    *,
    db: Session = Depends(get_db),
    strength:schemas.StrengthUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.strengths.update(
        db=db,
        strength=strength,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="strength-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_strength(
    *,
    db: Session = Depends(get_db),
    strength:schemas.StrengthDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.strengths.delete(db=db,uuid=strength.uuid)
    return schemas.Msg(message=__(key="strength-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_strength(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.StrengthDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.strengths.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="strength-deleted-successfully"))




@router.get("/get-my-strengths", response_model=None)
async def get_all_my_strengths(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.strengths.get_my_strengths(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )


@router.get("/get_strengths_by_uuid",response_model=schemas.StrengthResponse)
async def get_strengths(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))

):
    data = crud.strengths.get_by_uuid(db=db,uuid=uuid)
    if data is None:
        raise HTTPException(status_code=404,detail=__(key="strength-not-found"))
    return data