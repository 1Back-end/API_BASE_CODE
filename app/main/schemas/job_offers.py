from datetime import datetime
from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional, List
from app.main.models.job_offers import ContractType, WorkMode
from app.main.schemas.user import AddedBy



class JobOffersBase(BaseModel):
    title:str
    description:str
    currency:str
    salary:float
    employment_type:ContractType
    posted_date:datetime
    expiration_date:datetime
    work_mode:WorkMode
    contact_email:EmailStr


class JobOffersCreate(JobOffersBase):
    pass

class JobOffersUpdate(BaseModel):
    uuid:str
    title:Optional[str]=None
    description:Optional[str]=None
    currency:Optional[str]=None
    salary:Optional[float]=None
    employment_type:Optional[ContractType]=None
    posted_date:Optional[datetime]=None
    expiration_date:Optional[datetime]=None
    work_mode:Optional[WorkMode]=None
    contact_email:Optional[EmailStr]=None


class JobOffersResponse(BaseModel):
    uuid:str
    title:str
    description:str
    full_salary:Optional[str]=None
    employment_type:ContractType
    posted_date:datetime
    expiration_date:datetime
    work_mode:WorkMode
    contact_email:EmailStr
    created_at:datetime
    updated_at:datetime
    status:str
    model_config = ConfigDict(from_attributes=True)


class CompanySlim(BaseModel):
    uuid: str
    name: str
    email: str
    phone: str
    description: Optional[str] = None
    slogan: Optional[str] = None
    website: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AddedByCompany(BaseModel):
    uuid: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    company: Optional[List[CompanySlim]] = None

    model_config = ConfigDict(from_attributes=True)
class JobOffersResponseSlim1(BaseModel):
    uuid:str
    title:str
    description:str
    full_salary:Optional[str]=None
    employment_type:ContractType
    posted_date:datetime
    expiration_date:datetime
    work_mode:WorkMode
    contact_email:EmailStr
    created_at:datetime
    updated_at:datetime
    owner:Optional[AddedByCompany]=None
    model_config = ConfigDict(from_attributes=True)



class JobOffersUpdateStatus(BaseModel):
    uuid:str
class JobOffersDetails(BaseModel):
    uuid:str

class JobOffersDelete(BaseModel):
    uuid:str

class JobOffersResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[JobOffersResponse]

    model_config = ConfigDict(from_attributes=True)





class JobOffersResponseListSlim1(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[JobOffersResponseSlim1]

    model_config = ConfigDict(from_attributes=True)



class JobOffersSlim(BaseModel):
    uuid:str
    title:str
    description:str
    full_salary:Optional[str]
    employment_type:ContractType
    posted_date:datetime
    expiration_date:datetime
    work_mode:WorkMode
    contact_email:EmailStr
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)


class JobOffersSlim1(BaseModel):
    uuid:str
    title:str
    description:str
    full_salary:Optional[str]
    employment_type:ContractType
    posted_date:datetime
    expiration_date:datetime
    work_mode:WorkMode
    contact_email:EmailStr
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)



