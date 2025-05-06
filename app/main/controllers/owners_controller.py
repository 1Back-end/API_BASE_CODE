import uuid
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(prefix="/owners", tags=["owners"])

@router.post("/create", response_model=schemas.Owner, status_code=201)
def create(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.OwnerCreate,
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

    return crud.owner.create(db=db, obj_in=obj_in,added_by_uuid=added_by_uuid)


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
    order:str = Query(None, enum =["ASC","DESC"]),
    status: str = Query(None, enum =["ACTIVED","UNACTIVED","DELETED","BLOCKED"]),
    keyword:Optional[str] = None,
    # order_filed: Optional[str] = None
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    get administrator with all data by passing filters
    """
    
    return crud.owner.get_many(
        db, 
        page, 
        per_page, 
        order,
        status,
        # order_filed
        keyword
    )
    
@router.put("/{uuid}/status", response_model=schemas.OwnerResponse, status_code=200)
def update(
        uuid: str,
        status: str = Query(None, enum =["ACTIVED","UNACTIVED","BLOCKED"]),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):

    return crud.owner.update_status(db=db,uuid=uuid,status=status)

@router.delete("/{uuid}/delete", response_model=schemas.Msg)
def delete(
    *,
    db: Session = Depends(get_db),
    uuid: str,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    """
    Delete administrator
    """
    crud.owner.soft_delete(db, uuid)
    return {"message": __(key="owner-deleted")}
