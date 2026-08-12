from datetime import datetime,timezone

from sqlmodel import SQLModel,Field

class Candidate(SQLModel,table=True):
    id: int | None=Field(default=None,primary_key=True)
    name:str
    email:str |None=None
    phone:str |None=None
    skills:str|None=None
    projects:str|None=None
    education:str|None=None
    experience:str|None=None
    created_at:datetime =Field(default_factory=lambda:datetime.now(timezone.utc))
