from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity 

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

candidate_text = (
    "Build React and TypeScript features for a customer operations platform used by support and account teams."
)

jd_concepts = [
    "REST API development",
    "Python",
    "FastAPI",
    "customer-facing applications",
]

candidate_embedding = model.encode([candidate_text])

for concept in jd_concepts:
    concept_embedding = model.encode([concept])

    similarity = cosine_similarity(
        concept_embedding,
        candidate_embedding
    )[0][0]

    print(f"{concept}: {similarity:.4f}")