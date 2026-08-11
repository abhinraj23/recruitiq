from fastapi import APIRouter,Depends
from sqlmodel import Session

from app.schemas.job import JDRequest
from app.services.job_extractor import extract_job_profile
from app.db.session import get_session
from app.models.job import Job

router=APIRouter(
    prefix="/jobs",
    tags=["Jobs"]

)

@router.post("/extract")
async def extract_job(request:JDRequest,session:Session=Depends(get_session)):
    job_profile=extract_job_profile(request.description)

    job=Job(
        title=job_profile.title,
        experience_years=job_profile.experience_years,
        required_skills=",".join(job_profile.required_skills),
        preferred_skills=",".join(job_profile.preferred_skills),
        qualifications=",".join(job_profile.qualifications),
        responsibilities=",".join(job_profile.responsibilities)
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    return job