from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import get_embedding


router = APIRouter(
    prefix="/embedding",
    tags=["Embedding"]
)


class EmbeddingRequest(BaseModel):
    text: str


@router.post("/embed")
def create_embedding(request: EmbeddingRequest):
    return {
        "embedding": get_embedding(request.text)
    }


@router.get("/health")
def embedding_health():
    return {"status": "ok"}