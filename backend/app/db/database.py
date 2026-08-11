from sqlmodel import SQLModel,create_engine
from app.core.config import settings
from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job

engine=create_engine(
    settings.DATABASE_URL,
    echo=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)