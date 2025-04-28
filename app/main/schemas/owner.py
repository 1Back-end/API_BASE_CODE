from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from app.main.schemas import UserAuthentication, File, DataList
from app.main.schemas.file import FileSlim
from app.main.schemas.user import AddedBy

class Owner(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: Optional[str]
    lastname: str
    status: str
    avatar: Optional[FileSlim]
    creator: Optional[AddedBy]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)

class OwnerSlim(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: Optional[str]
    lastname: str
    status: str
    full_phone_number: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class OwnerResponse(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: Optional[str]
    lastname: str
    status: str
    full_phone_number: Optional[str]
    is_new_user: Optional[bool] = False
    avatar: Optional[File]
    added_by: Optional[AddedBy]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class OwnerSchemaBase(BaseModel):
    firstname: Optional[str] = None
    lastname: str
    email: EmailStr
    avatar_uuid: Optional[str] = None
    phone_number: Optional[str] = None


class OwnerCreate(OwnerSchemaBase):
    pass
    


class OwnerSchemaUpdate(BaseModel):
    uuid:str
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    avatar_uuid: Optional[str] = None
    phone_number: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OwnerSchemaDelete(BaseModel):
    uuid:str

class OwnerSchemasStatus(BaseModel):
    uuid:str
    status:str

class OwnerResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Owner]

    model_config = ConfigDict(from_attributes=True)

