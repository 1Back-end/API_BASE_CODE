from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class HobbyBase(BaseModel):
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class HobbyCreate(HobbyBase):
     pass

class HobbyUpdate(HobbyBase):
    uuid:str
    title: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class HobbyResponse(BaseModel):
    uuid:str
    title: str
    description: Optional[str] = None
    date_added :datetime
    date_modified :Optional[datetime] = None

   
    model_config = ConfigDict(from_attributes=True)



class HobbyDelete(BaseModel):
    uuid:str

class HobbyResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[HobbyResponse]

    model_config = ConfigDict(from_attributes=True)

     





