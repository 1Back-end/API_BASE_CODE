from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional
from datetime import datetime

from app.main.schemas.candidates import CandidateSlim
from app.main.schemas.file import FileSlim1
from app.main.schemas.job_offers import JobOffersSlim, JobOffersSlim1

class ApplicationBase(BaseModel):
    job_offer_uuid:str
    cover_letter_uuid:str
    cv_uuid:str

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationDetails(BaseModel):
    uuid:str

class ApplicationResponse(BaseModel):
    uuid:str
    candidate:CandidateSlim
    cv:FileSlim1
    cover_letter:FileSlim1
    applied_date:datetime
    status:str
    job_offer:JobOffersSlim
    
    
    model_config = ConfigDict(from_attributes=True)

class ApplicationResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[ApplicationResponse]

    model_config = ConfigDict(from_attributes=True)








class ApplicationResponseSlim1(BaseModel):
    uuid:str
    candidate:CandidateSlim
    job_offer:JobOffersSlim1
    cover_letter:FileSlim1
    cv:FileSlim1
    applied_date:datetime
    status:str
    model_config = ConfigDict(from_attributes=True)


class ApplicationResponseListSlim(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[ApplicationResponseSlim1]

    model_config = ConfigDict(from_attributes=True)



