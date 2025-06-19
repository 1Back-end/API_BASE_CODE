from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


from app.main.models.personals import GenderEnum

class PersonalBase(BaseModel):
    gender: GenderEnum
    professional_title: str
    title_description: Optional[str] = None
    birth_date: datetime
    place_of_birth: str
    region_of_origin: str
    adress: str
    nationality: str
    city: str
    country: str
    others: Optional[str] = None
    

    model_config = ConfigDict(from_attributes=True)

class PersonalCreate(PersonalBase):
     pass

class PersonalUpdate(PersonalBase):
    uuid:str
    gender: Optional[GenderEnum] = None
    professional_title: Optional[str] = None
    title_description: Optional[str] = None
    birth_date: Optional[datetime] = None
    place_of_birth: Optional[str] = None
    region_of_origin: Optional[str] = None
    adress: Optional[str] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    others: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PersonalResponse(BaseModel):
    uuid:str
    gender: GenderEnum
    professional_title: str
    title_description: Optional[str] = None
    birth_date: datetime
    place_of_birth: str
    region_of_origin: str
    adress: str
    nationality: str
    city: str
    country: str
    others: Optional[str] = None
    
    date_added :datetime
    date_modified :Optional[datetime] = None

   
    model_config = ConfigDict(from_attributes=True)




class PersonalDelete(BaseModel):
    uuid:str

class PersonalResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[PersonalResponse]

    model_config = ConfigDict(from_attributes=True)

     