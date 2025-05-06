from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from app.main.schemas import UserAuthentication, File, DataList
from app.main.schemas.user import AddedBy

class Owner(BaseModel):
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
    avatar_uuid: Optional[str] = None
    country_code:str
    phone_number: Optional[str] = None


class OwnerCreate(OwnerSchemaBase):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class OwnerUpdateBase(BaseModel):
    email: EmailStr
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    avatar_uuid: Optional[str] = None
    country_code:str
    phone_number: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class OwnerProfile(BaseModel):
    uuid: Optional[str] = None
    email: EmailStr
    firstname: Optional[str]
    lastname: str
    status: str
    full_phone_number: Optional[str]
    is_new_user: Optional[bool] = False
    avatar: Optional[File]
    

    model_config = ConfigDict(from_attributes=True)

class OwnerUpdate(OwnerUpdateBase):
    uuid: str


class OwnerDelete(BaseModel):
    uuid: list[str]


class OwnerList(DataList):
    data: list[Owner]

    model_config = ConfigDict(from_attributes=True)
class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OwnerAuthentication(BaseModel):
    owner: OwnerSlim
    token: Optional[Token] = None
    model_config = ConfigDict(from_attributes=True)

class OwnerResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Owner]

    model_config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordOption2Step1(BaseModel):
    email: EmailStr

class ResetPasswordOption2Step2(BaseModel):
    email: str
    otp: str

class ResetPasswordOption3Step3(BaseModel):
    email: str
    otp: str
    new_password:str
