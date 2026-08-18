from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select

from app.models.candidate import Candidate
from app.services.matcher import candidate_to_job
from app.schemas.job import JDRequest
from app.services.job_extractor import extract_job_profile
from app.services.candidate_retrieval import retrieve_and_rank_candidates
from app.services.interview_service import generate_interview_questions
from app.services.rag_service import generate_candidate_analysis
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

@router.get("/{job_id}/match/{candidate_id}")
def match_job_candidate(job_id:int,candidate_id:int,session:Session=Depends(get_session)):
    
    job=session.get(Job,job_id)
    candidate=session.get(Candidate,candidate_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="job not found"
        )
    
    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
            )
    
    return candidate_to_job(candidate,job)

@router.get("/{job_id}/search")
def search_job_candidates(job_id:int,top_k:int=5,session:Session=Depends(get_session)):

    job=session.get(Job,job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="job not found"
        )
    
    return retrieve_and_rank_candidates(job,top_k=top_k)

@router.get("/{job_id}/analysis")
def analyse_job(job_id:int,top_k:int=5,session:Session=Depends(get_session)):

    job=session.get(Job,job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="job not found"
        )
    return {
        "job_id":job_id,
        "analysis":generate_candidate_analysis(
            job,
            top_k=top_k
        )
    }

@router.get("/{job_id}/candidates/{candidate_id}/interview")
def generate_candidate_interview(
    job_id:int,
    candidate_id:int,
    session:Session=Depends(get_session)):

    job=session.get(Job,job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="job not found"
        )
    
    candidate=session.get(Candidate,candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="candidate not found"
        )
    
    return {
        "candidate_id":candidate_id,
        "job_id":job_id,
        "interview":generate_interview_questions(
            job,
            candidate_id
        )
    }

