from datetime import timedelta, datetime
from typing import Any,List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/personals", tags=["personals"])

@router.post("/create",response_model=schemas.Msg)
async def create_personal(
    *,
    db: Session = Depends(get_db),
    personal:schemas.PersonalCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.personals.create(
        db=db,
        obj_in=personal,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="personal-information-created-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_personal(
    *,
    db: Session = Depends(get_db),
    personal:schemas.PersonalUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.personals.update(
        db=db,
        personal=personal,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="personal-information-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_personal(
    *,
    db: Session = Depends(get_db),
    personal:schemas.PersonalDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.personals.delete(db=db,uuid=personal.uuid)
    return schemas.Msg(message=__(key="personal-information-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_personal(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.PersonalDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.personals.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="personal-information-deleted-successfully"))




@router.get("/get-my-personals", response_model=None)
async def get_all_my_personals(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.personals.get_my_personals(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )

@router.get("/get_personals_by_uuid",response_model=schemas.PersonalResponse)
async def get_personal(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))

):
   
    data = crud.personals.get_by_uuid(db=db,uuid=uuid)
    if data is None:
        raise HTTPException(status_code=404,detail=__(key="personal-information-not-found"))
    return data