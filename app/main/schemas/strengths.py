from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class StrengthBase(BaseModel):
    title: str
    level: int
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StrengthCreate(StrengthBase):
     pass

class StrengthUpdate(StrengthBase):
    uuid:str
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StrengthResponse(BaseModel):
    uuid:str
    title: str
    level: int
    description: Optional[str] = None
    date_added :datetime
    date_modified :Optional[datetime] = None

   
    model_config = ConfigDict(from_attributes=True)



class StrengthDelete(BaseModel):
    uuid:str

class StrengthResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[StrengthResponse]

    model_config = ConfigDict(from_attributes=True)

     