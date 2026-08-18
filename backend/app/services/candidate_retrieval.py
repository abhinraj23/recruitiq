from sqlmodel import Session

from app.db.database import engine
from app.models.candidate import Candidate
from app.services.matcher import candidate_to_job
from app.services.vector_store import search_candidates_for_job


def retrieve_and_rank_candidates(job, top_k: int = 5):

    results = search_candidates_for_job(
        job,
        top_k=top_k
    )

    candidate_ids =results["ids"][0]
    distances = results["distances"][0]

    ranked_candidates = []

    with Session(engine) as session:

        for candidate_id,distance in zip(candidate_ids,distances):

            candidate = session.get(
                Candidate,
                candidate_id
            )

            if not candidate:
                continue

            score = candidate_to_job(
                candidate,
                job
            )

            ranked_candidates.append({
                "candidate_id": int(candidate_id),
                "semantic_distance":distance,
                "name": candidate.name,
                "skills": candidate.skills,
                "experience": candidate.experience,
                "projects": candidate.projects,
                "education": candidate.education,
                **score
            })

    ranked_candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_candidates