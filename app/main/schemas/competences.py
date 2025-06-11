from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class CompetenceBase(BaseModel):
    title: str
    level: str
    years_of_experience: int
    is_certified: Optional[bool] = None
    description: Optional[str] = None
    category: str 

    model_config = ConfigDict(from_attributes=True)

class CompetenceCreate(CompetenceBase):
     candidat_iuud: int

class CompetenceUpdate(CompetenceBase):
    uuid:str
    title: Optional[str] = None
    level: Optional[str] = None
    years_of_experience: Optional[int] = None
    is_certified: Optional[bool] = None
    description: Optional[str] = None
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CompetenceResponse(BaseModel):
    uuid:str
    title: str
    level: str 
    years_of_experience: int 
    is_certified: bool 
    description: str 
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)






class CompetenceDelete(BaseModel):
    uuid:str

class JobOffersResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[CompetenceResponse]

    model_config = ConfigDict(from_attributes=True)

     