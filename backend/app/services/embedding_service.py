import os

import chromadb
from sentence_transformers import SentenceTransformer
from sqlmodel import Session, select
import dotenv

from app.db.database import engine
from app.models.candidate import Candidate
from app.services.vector_store import build_candidate_document

dotenv.load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)


client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT
)

candidate_collection = client.get_or_create_collection(
    name="candidates"
)

model = SentenceTransformer(MODEL_NAME)


def index_candidates():

    with Session(engine) as session:

        candidates = session.exec(
            select(Candidate)
        ).all()

        print("Starting embedding...")

        for candidate in candidates:

            document = build_candidate_document(candidate)

            print(f"Embedding candidate {candidate.id}...")

            embedding = model.encode(
                document
            ).tolist()

            candidate_collection.upsert(
                ids=[str(candidate.id)],
                documents=[document],
                embeddings=[embedding],
                metadatas=[
                    {
                        "candidate_id": candidate.id,
                        "name": candidate.name or "",
                    }
                ]
            )

            print(f"Indexed candidate {candidate.id}")

        print(f"Indexed {len(candidates)} candidates")


if __name__ == "__main__":
    index_candidates()