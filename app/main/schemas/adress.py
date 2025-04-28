from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from app.main.schemas import UserAuthentication, File, DataList
from app.main.schemas.file import FileSlim
from app.main.schemas.user import AddedBy

class Adress(BaseModel):
    uuid: Optional[str] = None
    street: str
    city: Optional[str]
    state: str
    zipcode: str
    country: Optional[FileSlim]
    apartment_number: Optional[AddedBy]
    additional_information: datetime
    date_added: datetime
    date_modified: datetime

    class AddressSchemaBase(BaseModel):
        street: str 
        city:str 
        state: str 
        zipcode: str 
        country: str 
        apartment_information: Optional[str]

class OwnerCreate(OwnerSchemaBase):
    pass

class AdressSchemaUpdate(BaseModel):
    uuid:str
    street:str = None
    city :str = None
    state:str = None
    zip_code:str = None
    country:str = None
    apart_number:str = None

class OwnerSchemaDelete(BaseModel):
    uuid:str


