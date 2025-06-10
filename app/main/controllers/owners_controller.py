import uuid
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.main.core.security import is_valid_password
router = APIRouter(prefix="/owners", tags=["owners"])

@router.post("/create", response_model=schemas.Msg, status_code=201)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.OwnerCreate,
):
    """
    Create owner
    """
    owner = crud.owner.get_by_email(db=db,email=obj_in.email)
    if owner:
        raise HTTPException(status_code=409, detail=__(key="owner-email-taken"))
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))
        
    exist_phone_number = crud.owner.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409,detail=__(key="phone-number-already-exist"))
    
    if not is_valid_password(obj_in.password_hash):
        raise HTTPException(status_code=400,detail=__(key="invalid-password"))

    crud.owner.create(db=db, obj_in=obj_in)
    return {"message": __(key="account-created-successfully")}



@router.put("/update",response_model=schemas.Owner,status_code=201)
def edit(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.OwnerUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    Create owner
    """
    added_by_uuid= current_user.uuid
    owner = crud.owner.get_by_email(db=db,email=obj_in.email)
    if owner:
        raise HTTPException(status_code=409, detail=__(key="owner-email-taken"))
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404, detail=__(key="avatar-not-found"))

    return crud.owner.update(db=db, obj_in=obj_in,added_by_uuid=added_by_uuid)

@router.get("/get_many", response_model=None)
def get(
    *,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 30,
    order:Optional[str] = Query(None, enum =["ASC","DESC"]),
    status: Optional[str] = Query(None, enum =["ACTIVED","UNACTIVED","DELETED","BLOCKED"]),
    keyword:Optional[str] = None,
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.owner.get_many(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        status=status,
        keyword=keyword,
    )
    
@router.put("/update-owner-status", response_model=schemas.Msg, status_code=200)
def update_owner_staus(
        *,
        db: Session = Depends(get_db),
        obj_in:schemas.OwnerSoftDelete,
        status: str = Query(None, enum =["ACTIVED","UNACTIVED","BLOCKED"]),
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):

    crud.owner.update_status(db=db,uuid=obj_in.uuid,status=status)
    return {"message": __(key="owner-status-updated-successfully")}


@router.put("/soft_delete", response_model=schemas.Msg)
def soft_delete_owner(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.OwnerSoftDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.owner.soft_delete(db=db, uuid=obj_in.uuid)
    return {"message": __(key="owner-deleted")}
