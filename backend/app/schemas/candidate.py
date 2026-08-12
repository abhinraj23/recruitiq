from pydantic import BaseModel,Field

class Experience(BaseModel):
    role: str
    company: str | None = None
    years: float | None = None
    responsibilities: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)

class Education(BaseModel):
    degree: str | None = None
    field: str | None = None
    institution: str | None = None
    graduation_year: int | None = None

class CandidateProfile(BaseModel):
    name:str
    email:str | None=None
    phone:str | None=None
    experience:list[Experience]=Field(default_factory=list)
    skills:list[str]=Field(default_factory=list)
    projects:list[Project]=Field(default_factory=list)
    education:list[Education]=Field(default_factory=list)

