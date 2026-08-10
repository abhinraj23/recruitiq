from fastapi import APIRouter,UploadFile,File,Depends
from sqlmodel import Session
from app.services.resume_parser import extract_text_from_pdf
from app.services.candidate_extractor import extract_candidate_profile
from app.db.session import get_session
from app.models.candidate import Candidate

router=APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

@router.post("/upload")
async def upload_resume(file:UploadFile=File(...),session:Session=Depends(get_session)):

    file_content=await file.read()

    with open(file.filename,"wb") as buffer:
        buffer.write(file_content)

    extracted_text=extract_text_from_pdf(file.filename)

    candidate_profile=extract_candidate_profile(extracted_text)

    candidate=Candidate(
        name=candidate_profile.name,
        email=candidate_profile.email,
        phone=candidate_profile.phone,
        skills=",".join(candidate_profile.skills),
        projects=",".join(candidate_profile.projects),
        education=",".join(candidate_profile.education),
        experience_years=candidate_profile.experience_years
    )

    session.add(candidate)
    session.commit()
    session.refresh(candidate)

    return candidate
