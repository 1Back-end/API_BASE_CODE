from datetime import timedelta, datetime
from typing import Any,List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/medias", tags=["medias"])

@router.post("/create",response_model=schemas.Msg)
async def create_media(
    *,
    db: Session = Depends(get_db),
    media:schemas.MediaCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.medias.create(
        db=db,
        obj_in=media,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="social-media-added-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_media(
    *,
    db: Session = Depends(get_db),
    media:schemas.MediaUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.medias.update(
        db=db,
        media=media,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="social-media-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_media(
    *,
    db: Session = Depends(get_db),
    media:schemas.MediaDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.medias.delete(db=db,uuid=media.uuid)
    return schemas.Msg(message=__(key="social-media-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_media(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.MediaDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.medias.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="media-social-deleted-successfully"))




@router.get("/get-my-medias", response_model=None)
async def get_all_my_medias(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.medias.get_my_medias(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )

@router.get("/get_medias_by_uuid",response_model=schemas.MediaResponse)
async def get_media(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))

):
   
    data = crud.medias.get_by_uuid(db=db,uuid=uuid)
    if data is None:
        raise HTTPException(status_code=404,detail=__(key="social-media-not-found"))
    return data