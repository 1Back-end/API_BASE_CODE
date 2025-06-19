from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

from app.main.models.languages import LanguageType

class LanguageBase(BaseModel):
    title: str
    level: str
    is_certified: Optional[bool] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LanguageCreate(LanguageBase):
     pass

class LanguageUpdate(LanguageBase):
    uuid:str
    title: Optional[str] = None
    level: Optional[str] = None
    is_certified: Optional[bool] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LanguageResponse(BaseModel):
    uuid:str
    title: str
    level: str 
    is_certified: Optional[bool] = None
    description: Optional[str] = None
    date_added :datetime
    date_modified :Optional[datetime] = None

   
    model_config = ConfigDict(from_attributes=True)




class LanguageDelete(BaseModel):
    uuid:str

class LanguageResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[LanguageResponse]

    model_config = ConfigDict(from_attributes=True)

     