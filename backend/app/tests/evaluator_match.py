from sqlmodel import Session, select

from app.db.database import engine
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.matcher import candidate_to_job


def main():

    with Session(engine) as session:

        # Get the job we want to evaluate against
        job = session.get(Job,2)

        if not job:
            print("No job found.")
            return

        # Get all candidates
        candidates = session.exec(
            select(Candidate)
            .where(Candidate.id>=2)
        ).all()

        print(f"Job: {job.title}")
        print(f"Candidates: {len(candidates)}")
        print("-" * 90)

        for candidate in candidates:

            result = candidate_to_job(
                candidate,
                job
            )

            print(
                f"Candidate {candidate.id}: "
                f"Total={result['score']:.2f}, "
                f"Project={result['project_score']:.4f}, "
                f"Experience={result['experience_score']:.4f}, "
                f"Required={result['required_skill_score']:.4f}, "
                f"Preferred={result['preferred_skill_score']:.4f}, "
                f"Qualification={result['qualification_score']:.4f}"
            )


if __name__ == "__main__":
    main()