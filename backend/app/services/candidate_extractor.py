from google import genai

from app.core.config import settings
from app.schemas.candidate import CandidateProfile

client=genai.Client(api_key=settings.GEMINI_API_KEY)

def extract_candidate_profile(resume_text:str)->CandidateProfile:

    prompt=f"""
    Extract candidate information from the resume given below delimited by curly braces.

    Return:

    -name
    -email
    -phone
    -skills
    -projects
    -experience in years
    -education

    Resume:
    <{resume_text}>
    """

    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type":"application/json",
            "response_schema":CandidateProfile
        }
    )

    return CandidateProfile.model_validate_json(response.text)
