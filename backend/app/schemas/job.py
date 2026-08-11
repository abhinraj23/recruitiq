from pydantic import BaseModel,Field

class JobProfile(BaseModel):
    title:str
    experience_years:float|None=None
    required_skills:list[str]=Field(default_factory=list)
    preferred_skills:list[str]=Field(default_factory=list)
    qualifications:list[str]=Field(default_factory=list)
    responsibilities:list[str]=Field(default_factory=list)

class JDRequest(BaseModel):
    description:str