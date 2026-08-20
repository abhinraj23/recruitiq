import os

from sqlmodel import Session, create_engine, select, SQLModel
from dotenv import load_dotenv
from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job

load_dotenv()
# -----------------------------
# SOURCE: Local SQLite
# -----------------------------
SQLITE_URL = "sqlite:///recruitiq.db"
sqlite_engine = create_engine(SQLITE_URL)


# -----------------------------
# DESTINATION: Railway PostgreSQL
# -----------------------------
POSTGRES_URL = os.getenv("DATABASE_URL")

if POSTGRES_URL.startswith("postgres://"):
    POSTGRES_URL = POSTGRES_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif POSTGRES_URL.startswith("postgresql://"):
    if "+psycopg" not in POSTGRES_URL:
        POSTGRES_URL = POSTGRES_URL.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    
postgres_engine = create_engine(POSTGRES_URL)


# -----------------------------
# Create PostgreSQL tables
# -----------------------------
SQLModel.metadata.create_all(postgres_engine)


# -----------------------------
# Read data from SQLite
# -----------------------------
with Session(sqlite_engine) as sqlite_session:
    users = sqlite_session.exec(select(User)).all()
    candidates = sqlite_session.exec(select(Candidate)).all()
    jobs = sqlite_session.exec(select(Job)).all()


# -----------------------------
# Write data to PostgreSQL
# -----------------------------
with Session(postgres_engine) as postgres_session:

    # Production database is currently empty,
    # so clear any partially migrated records.
    postgres_session.exec(User.__table__.delete())
    postgres_session.exec(Candidate.__table__.delete())
    postgres_session.exec(Job.__table__.delete())

    # Preserve original IDs
    for user in users:
        postgres_session.add(user)

    for candidate in candidates:
        postgres_session.add(candidate)

    for job in jobs:
        postgres_session.add(job)

    postgres_session.commit()


print("Migration completed successfully.")
print(f"Users: {len(users)}")
print(f"Candidates: {len(candidates)}")
print(f"Jobs: {len(jobs)}")