from sqlmodel import Session, select

from app.db.database import engine
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.matcher import candidate_to_job


def main():

    DAY8_BASELINE = {
    2: 85.10,
    3: 69.26,
    4: 50.00,
    5: 66.71,
    6: 69.25,
    7: 78.45,
    8: 79.71,
    9: 55.95,
    10: 50.42,
    11: 64.61,}

    EXPECTED_RANKING = [
    1, 7, 6, 5, 2, 4, 10, 9, 3, 8]

    with Session(engine) as session:

        # Get the job we want to evaluate against
        job = session.get(Job,2)

        if not job:
            print("No job found.")
            return

        # Get all candidates
        candidates = session.exec(
            select(Candidate)
            .where(Candidate.id>=2,Candidate.id<=11)
        ).all()

        print(f"Job: {job.title}")
        print(f"Candidates: {len(candidates)}")
        print("-" * 90)

        results=[]

        for test_number,candidate in enumerate(candidates,start=1):

            result = candidate_to_job(
                candidate,
                job
            )

            baseline = DAY8_BASELINE[candidate.id]
            change = result["score"] - baseline

            results.append({
                "test_number": test_number,
                "candidate_id": candidate.id,
                "score": result["score"],})

            print(
                f"Test candidate {test_number} "
                f"(DB ID {candidate.id}): "
                f"Total={result['score']:.2f}, "
                f"Day8={baseline:.2f}, "
                f"Change={change:+.2f}, "
                f"Project={result['project_score']:.4f}, "
                f"Experience={result['experience_score']:.4f}, "
                f"Required={result['required_skill_score']:.4f}, "
                f"Preferred={result['preferred_skill_score']:.4f}, "
                f"Qualification={result['qualification_score']:.4f}"
            )
    results.sort(key=lambda item:item["score"],reverse=True)

    actual_ranking = [item["test_number"] for item in results ]

    print("\nExpected ranking:")
    print(" > ".join(map(str, EXPECTED_RANKING)))

    print("\nActual ranking:")
    print(" > ".join(map(str, actual_ranking)))


if __name__ == "__main__":
    main()