import os
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

load_dotenv()

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def get_embedding(text: str):
    return get_model().encode(text).tolist()