from google import genai

from app.core.config import settings
from app.schemas.candidate import CandidateProfile

client=genai.Client(api_key=settings.GEMINI_API_KEY)

def extract_candidate_profile(resume_text:str)->CandidateProfile:

    prompt=f"""
    Extract structured candidate information from the resume given below delimited by curly braces.
    
    Extract the folllowing:

    1.Candidate name,email and phone number
    2.Technical and professional skills
    3.Every relevant work experience:
    -role or job title
    -company
    -approximate years of duration
    -responsibilities
    4.Projects mentioned in the resume:
    -title
    -description
    -technologies used
    5.Educational qualifications:
    -degree
    -field
    -institution
    -graduated_year

    Important:
    -Only extract information supported by the resume.
    -Do not invent missing informations
    -If a field is not available, return an empty list or null where appropriate.

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
