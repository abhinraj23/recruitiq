import chromadb
from sentence_transformers import SentenceTransformer
from sqlmodel import Session,select
import os
from dotenv import load_dotenv

from app.models.candidate import Candidate
from app.core.config import settings
from app.models.job import Job
from app.db.database import engine
from app.services.matcher import candidate_to_job


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

_embedding_model = None

def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    
    return _embedding_model

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

    embedding=get_embedding_model().encode(
        document
    ).tolist()

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

    query_embedding = get_embedding_model().encode(
        query
    ).tolist()

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

    
    

