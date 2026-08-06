from fastapi import APIRouter

router=APIRouter()

@router.get("/")
def root():
    return {
        "message":"Welcome to RecruitIQ",
        "version":"1.0.0",
        "status":"healthy"
    }