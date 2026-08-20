from sqlmodel import SQLModel,create_engine
from app.core.config import settings
from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job

database_url = settings.DATABASE_URL

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(
    database_url,
    echo=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)