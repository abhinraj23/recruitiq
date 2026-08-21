import chromadb
from sqlmodel import Session,select
import os
import httpx
from dotenv import load_dotenv

from app.models.candidate import Candidate
from app.core.config import settings
from app.models.job import Job
from app.db.database import engine
from app.services.matcher import candidate_to_job

load_dotenv()

CHROMA_HOST = settings.CHROMA_HOST
CHROMA_PORT = settings.CHROMA_PORT

if CHROMA_HOST:
    client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
    )
else:
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

candidate_collections=client.get_or_create_collection(
    name="candidates"
)

EMBEDDING_SERVICE_URL = os.getenv(
    "EMBEDDING_SERVICE_URL"
)


def get_embedding(text: str):
    response = httpx.post(
        f"{EMBEDDING_SERVICE_URL}/embedding/embed",
        json={"text": text},
        timeout=120.0
    )

    response.raise_for_status()

    return response.json()["embedding"]

def build_candidate_document(candidate) -> str:

    return f"""
    Candidate: {candidate.name or ""}

    Skills:
    {candidate.skills or ""}

    Experience:
    {candidate.experience or ""}

    Projects:
    {candidate.projects or ""}

    Education:
    {candidate.education or ""}
    """.strip()

def build_job_query(job) -> str:
    return f"""
    Job Title:
    {job.title or ""}

    Required Skills:
    {job.required_skills or ""}

    Preferred Skills:
    {job.preferred_skills or ""}

    Experience:
    {job.experience_years or ""} years

    Qualifications:
    {job.qualifications or ""}

    Responsibilities:
    {job.responsibilities or ""}
    """.strip()


def add_candidate(candidate):

    document=build_candidate_document(candidate)

    embedding = get_embedding(document)

    candidate_collections.upsert(
        ids=[str(candidate.id)],
        documents=[document],
        embeddings=[embedding],
        metadatas=[
            {
                "candidate_id":candidate.id,
                "name":candidate.name or "",
            }
        ]
    )

def index_test_candidates():

    with Session(engine) as session:

        candidates=session.exec(
            select(Candidate)
        ).all()

        for candidate in candidates:
            add_candidate(candidate)
        
        print(f"indexed {len(candidates)} candidates")


def search_candidates(query: str, top_k: int = 5):

    query_embedding = get_embedding(query)

    results = candidate_collections.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results

def search_candidates_for_job(job, top_k: int = 5):

    query = build_job_query(job)

    return search_candidates(
        query,
        top_k=top_k
    )


