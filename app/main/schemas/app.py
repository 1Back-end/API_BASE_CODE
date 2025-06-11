class Candidate(CandidateResponse):
    uuid: str
    experiences: List[Experience] = []
    diplomas: List[Diploma] = []
    graduation_year:str
    model_config = ConfigDict(from_attributes=True)


class CandidateResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: List[Candidate]
    model_config = ConfigDict(from_attributes=True)


class CandidateSlim(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    code_country: str
    phone_number: str
    full_phone_number: str
    address: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# --- Authentication Models ---
class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class CandidateAuthentication(BaseModel):
    candidat: CandidateSlim
    token: Optional[Token] = None
    model_config = ConfigDict(from_attributes=True)


class CandidateLogin(BaseModel):
    email: EmailStr
    password: str
