from langchain_core.prompts import ChatPromptTemplate
from sqlmodel import Session
import json

from app.db.database import engine
from app.models.candidate import Candidate
from app.services.rag_service import llm
from app.services.matcher import candidate_to_job



interview_prompt = ChatPromptTemplate.from_template(
    """
You are an expert technical interviewer.

Generate a structured interview plan for the candidate below
based on the specific job requirements.

Job:
{job}

Candidate:
{candidate}

Generate exactly:

- 3 technical questions
- 2 experience-based questions
- 1 question about a potential gap or weakness

For every question provide:

- title: a short descriptive title
- question: the actual interview question
- what_to_assess: what the interviewer should evaluate from the candidate's answer

Rules:

1. Use only information provided about the candidate and job.
2. Do not invent candidate experience, skills, projects, or achievements.
3. Questions should be specific to this candidate and this job.
4. Keep questions professional and suitable for a real technical interview.
5. Do not include introductory text, explanations, Markdown, or headings outside the JSON.
6. Return ONLY valid JSON.

Use exactly this JSON structure:

{{
  "technical": [
    {{
      "title": "string",
      "question": "string",
      "what_to_assess": "string"
    }}
  ],
  "experience": [
    {{
      "title": "string",
      "question": "string",
      "what_to_assess": "string"
    }}
  ],
  "potential_gaps": [
    {{
      "title": "string",
      "question": "string",
      "what_to_assess": "string"
    }}
  ]
}}
"""
)

def build_interview_context(job,candidate_id:int):

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

    content = response.content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.endswith("```"):
        content = content[:-3]

    return json.loads(content.strip())