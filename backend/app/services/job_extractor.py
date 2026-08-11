from google import genai

from app.core.config import settings
from app.schemas.job import JobProfile

client=genai.Client(api_key=settings.GEMINI_API_KEY)

def extract_job_profile(job_text:str)->JobProfile:

    prompt=f"""
    Extract the job details from the given job description.
    return in the structured json format.

    job description:
    {job_text}

    """
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type":"application/json",
            "response_schema":JobProfile

        }
    )

    return JobProfile.model_validate_json(response.text)