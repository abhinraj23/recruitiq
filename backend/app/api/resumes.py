from fastapi import APIRouter,UploadFile,File
from app.services.resume_parser import extract_text_from_pdf
from app.services.candidate_extractor import extract_candidate_profile

router=APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

@router.post("/upload")
async def upload_resume(file:UploadFile=File(...)):

    file_content=await file.read()

    with open(file.filename,"wb") as buffer:
        buffer.write(file_content)

    extracted_text=extract_text_from_pdf(file.filename)

    candidate_profile=extract_candidate_profile(extracted_text)

    return candidate_profile
