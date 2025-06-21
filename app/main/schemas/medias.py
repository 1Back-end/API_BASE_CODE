from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime

class MediaBase(BaseModel):
    title: str
    link: str
    

    model_config = ConfigDict(from_attributes=True)

class MediaCreate(MediaBase):
    pass

class MediaUpdate(MediaBase):
    uuid:str
    title: Optional[str] = None
    link: Optional[str] = None


    model_config = ConfigDict(from_attributes=True)

class MediaResponse(BaseModel):
    uuid:str
    title: str
    link: str
    date_added :datetime
    date_modified :Optional[datetime] = None

   
    model_config = ConfigDict(from_attributes=True)



class MediaDelete(BaseModel):
    uuid:str

class MediaResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[MediaResponse]

    model_config = ConfigDict(from_attributes=True)

     





