from fastapi import APIRouter

from pydantic import BaseModel

from app.services.enquiry_service import generate_enquiry_answer


router=APIRouter(
    prefix="/enquiry",
    tags=["enquiry"]
)

class EnquiryRequest(BaseModel):
    question:str

@router.post("/")
def enquiry(request:EnquiryRequest):

    try:
        answer = generate_enquiry_answer(question=request.question,top_k=5,)

        return {"question": request.question,"answer": answer}

    except Exception as e:
        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return {
                "question": request.question,
                "error": "AI service quota temporarily exceeded.",
            }

        raise