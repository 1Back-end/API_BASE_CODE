from datetime import timedelta, datetime
from typing import Any,List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/languages", tags=["languages"])

@router.post("/create",response_model=schemas.Msg)
async def create_language(
    *,
    db: Session = Depends(get_db),
    language:schemas.LanguageCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.languages.create(
        db=db,
        language=language,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="language-added-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_language(
    *,
    db: Session = Depends(get_db),
    language:schemas.LanguageUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.languages.update(
        db=db,
        language=language,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="language-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_language(
    *,
    db: Session = Depends(get_db),
    language:schemas.LanguageDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.languages.delete(db=db,uuid=language.uuid)
    return schemas.Msg(message=__(key="language-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_language(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.LanguageDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.languages.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="language-deleted-successfully"))




@router.get("/get-my-languages", response_model=None)
async def get_all_my_languages(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.languages.get_my_languages(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )

@router.get("/get_languages_by_uuid",response_model=schemas.LanguageResponse)
async def get_language(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))

):
    data = crud.languages.get_by_uuid(db=db,uuid=uuid)
    if data is None:
        raise HTTPException(status_code=404,detail=__(key="language-not-found"))
    return data