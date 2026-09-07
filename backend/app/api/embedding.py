from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import (get_embedding,get_embeddings)



router = APIRouter(
    prefix="/embedding",
    tags=["Embedding"]
)


class EmbeddingRequest(BaseModel):
    text: str


class BatchEmbeddingRequest(BaseModel):
    texts: list[str]



@router.post("/embed")
def create_embedding(request: EmbeddingRequest):
    return {
        "embedding": get_embedding(request.text)
    }

@router.post("/embed-batch")
def create_batch_embeddings(request: BatchEmbeddingRequest):
    return {
        "embeddings": get_embeddings(request.texts)
    }


@router.get("/health")
def embedding_health():
    return {"status": "ok"}