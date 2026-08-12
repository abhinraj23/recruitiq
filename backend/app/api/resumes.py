from fastapi import APIRouter,UploadFile,File,Depends
from sqlmodel import Session
import json

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
        skills=json.dumps(candidate_profile.skills),
        projects=json.dumps([project.model_dump() for project in candidate_profile.projects]),
        education=json.dumps([education.model_dump() for education in candidate_profile.education]),
        experience=json.dumps([experience.model_dump() for experience in candidate_profile.experience])
    )

    session.add(candidate)
    session.commit()
    session.refresh(candidate)

    return candidate
