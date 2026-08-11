from datetime import datetime,timezone

from sqlmodel import SQLModel,Field

class Job(SQLModel,table=True):
    id:int|None =Field(default=None,primary_key=True)
    title:str
    experience_years:float|None=None
    required_skills:str|None
    preferred_skills:str|None
    qualifications:str|None
    responsibilities:str|None
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
