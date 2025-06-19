from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/hobbies", tags=["hobbies"])

@router.post("/create",response_model=schemas.Msg)
async def create_hobby(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.HobbyCreate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.hobbies.create(
        db=db,
        obj_in=obj_in,
        candidate_uuid=current_user.uuid
    )
    return schemas.Msg(message=__(key="hobby-created-successfully"))



@router.put("/update",response_model=schemas.Msg)
def update_hobby(
    *,
    db: Session = Depends(get_db),
    hobby:schemas.HobbyUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.hobbies.update(
        db=db,
        hobby=hobby,
        candidate_uuid=current_user.uuid  
    )

    return schemas.Msg(message=__(key="hobby-updated-successfully"))


@router.delete("/delete-drop",response_model=schemas.Msg)
async def delete_hobby(
    *,
    db: Session = Depends(get_db),
    hobby:schemas.HobbyDelete,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
    
):
    crud.hobbies.delete(db=db,uuid=hobby.uuid)
    return schemas.Msg(message=__(key="hobby-deleted-successfully"))




@router.put("/soft_delete", response_model=schemas.Msg)
async def soft_delete_hobby(
        *,
        db: Session = Depends(get_db),
        obj_in: schemas.HobbyDelete,
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    crud.hobbies.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="hobby-deleted-successfully"))




@router.get("/get-my-hobbies", response_model=None)
async def get_all_my_hobbies(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        keyword: Optional[str] = None,
        order_field: Optional[str] = None,  # Correction de order_filed → order_field
        current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))
):
    return crud.hobbies.get_my_hobbies(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,  # Correction ici aussi
        keyword=keyword,
        candidate_uuid=current_user.uuid,

    )


@router.get("/get_hobbies_by_uuid",response_model=schemas.HobbyResponse)
async def get_hobby(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user: models.User = Depends(TokenRequired(roles=["CANDIDATE"]))

):
    data = crud.hobbies.get_by_uuid(db=db,uuid=uuid)
    if data is None:
        raise HTTPException(status_code=404,detail=__(key="hobby-not-found"))
    return data