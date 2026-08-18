from langchain_core.prompts import ChatPromptTemplate
from sqlmodel import Session

from app.db.database import engine
from app.models.candidate import Candidate
from app.services.rag_service import llm
from app.services.matcher import candidate_to_job



interview_prompt = ChatPromptTemplate.from_template(
    """
You are an expert technical interviewer.

Generate interview questions for the candidate below
based on the specific job requirements.

Job:
{job}

Candidate:
{candidate}

Generate:
1. Three technical questions.
2. Two experience-based questions.
3. One question about a potential gap or weakness.

For every question, briefly explain why it is relevant.

Do not invent facts about the candidate.
Use only the information provided.
"""
)

def build_interview_context(job,candidate_id:int)->str:

    with Session(engine) as session:
        candidate=session.get(Candidate,candidate_id)
    
    if not candidate:
        raise ValueError(
            "candidate not found"
        )
    
    score = candidate_to_job(
            candidate,
            job
        )

    return f"""
    Candidate ID: {candidate.id}
    Name: {candidate.name}

    Skills:
    {candidate.skills}

    Experience:
    {candidate.experience}

    Projects:
    {candidate.projects}

    Education:
    {candidate.education}

    Match Score:
    {score["score"]}

    Project Score:
    {score["project_score"]}

    Experience Score:
    {score["experience_score"]}
 
    Required Skills Score:
    {score["required_skill_score"]}

    Preferred Skills Score:
    {score["preferred_skill_score"]}

    Qualification Score:
    {score["qualification_score"]}
    """.strip()

def generate_interview_questions(job,candidate_id:int)->str:

    context=build_interview_context(
        job,
        candidate_id
    )

    job_context = f"""
    Title: {job.title}

    Required Skills:
    {job.required_skills}
 
    Preferred Skills: 
    {job.preferred_skills}

    Experience Required:
    {job.experience_years}

    Qualifications:
    {job.qualifications}

    Responsibilities:
    {job.responsibilities}
    """.strip()

    messages=interview_prompt.format_messages(
        candidate=context,
        job=job_context
    )

    response=llm.invoke(messages)

    return response.content