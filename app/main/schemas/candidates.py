from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date

from app.main.schemas.file import FileSlim1

# --- Candidate Models ---
class CandidateBase(BaseModel):
    civility:str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str

class CandidateSlim(BaseModel):
    civility: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    model_config = ConfigDict(from_attributes=True)

class CandidateCreate(CandidateBase):
    pass

class DiplomasBase(BaseModel):
    degree_name:str
    institution_name:str
    start_year:str
    end_year:str
    address:str
    model_config = ConfigDict(from_attributes=True)

class DiplomaCreate(DiplomasBase):
    pass

class DiplomasSlim(BaseModel):
    uuid:str
    degree_name:str
    institution_name:str
    start_year:str
    end_year:str
    address:str
    graduation_year : str
    date_added:datetime
    date_modified : Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class DiplomaUpdate(BaseModel):
    uuid:str
    degree_name:Optional[str]
    institution_name:Optional[str]
    start_year:Optional[str]
    end_year:Optional[str]
    address:Optional[str]

class DiplomaDelete(BaseModel):
    uuid:str


class DiplomaExperience(BaseModel):
    uuid:str

class ExperenciesBase(BaseModel):
    job_title : str
    company_name:str
    start_date:str
    end_date:str
    description:str
    model_config = ConfigDict(from_attributes=True)


class ExperenciesSlim(BaseModel):
    uuid:str
    job_title: str
    company_name: str
    start_date: str
    end_date: str
    description: str
    date_added : datetime
    date_modified : Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class ExperenciesCreate(ExperenciesBase):
    pass

class ExperenciesUpdate(BaseModel):
    uuid:str
    job_title:Optional[str]
    company_name:Optional[str]
    start_date:Optional[str]
    end_date:Optional[str]
    description:Optional[str]
    model_config = ConfigDict(from_attributes=True)

class DiplomaResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[DiplomasSlim]

    model_config = ConfigDict(from_attributes=True)


class ExperiencesResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[ExperenciesSlim]

    model_config = ConfigDict(from_attributes=True)











class LanguageSlim(BaseModel):
    uuid: str
    title: str
    level: str
    is_certified: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class HobbySlim(BaseModel):
    uuid: str
    title: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class PersonnalInformationSlim(BaseModel):
    gender: Optional[str] = None
    professional_title: Optional[str] = None
    title_description: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None
    region_of_origin: Optional[str] = None
    adress: Optional[str] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    others: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class Candidate(CandidateSlim):
    uuid: str
    diplomas: List[DiplomasBase] = []
    experiences : List[ExperenciesBase] = []
    model_config = ConfigDict(from_attributes=True)


class CandidateResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[Candidate]

    model_config = ConfigDict(from_attributes=True)
<<<<<<< Updated upstream
=======




class AllCandidate(CandidateSlim):
    uuid: str
    diplomas: List[DiplomasBase] = []
    experiences : List[ExperenciesBase] = []
    competences : List[CompetenceSlim] = []
    languages : List[LanguageSlim] = []
    hobbies : List[HobbySlim] = []
    personals : List[PersonnalInformationSlim] = []
    model_config = ConfigDict(from_attributes=True)


class AllCandidateResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[AllCandidate]

    model_config = ConfigDict(from_attributes=True)

>>>>>>> Stashed changes
