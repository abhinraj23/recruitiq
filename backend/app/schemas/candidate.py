from pydantic import BaseModel,Field

class CandidateProfile(BaseModel):
    name:str
    email:str | None=None
    phone:str | None=None
    experience_years:float | None=None
    skills:list[str]=Field(default_factory=list)
    projects:list[str]=Field(default_factory=list)
    education:list[str]=Field(default_factory=list)

