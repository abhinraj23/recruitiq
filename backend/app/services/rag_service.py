import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import json

from app.services.candidate_retrieval import retrieve_and_rank_candidates
from app.services.evidence_service import (
    build_skill_evidence,
    build_experience_evidence,
    build_project_evidence,
    build_qualification_evidence,
)
from app.services.matcher import parse_job_list
from app.models import job
from app.schemas import candidate
from app.schemas import candidate



load_dotenv()

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0

)

prompt=ChatPromptTemplate.from_template(
        """
        You are an explanation assistant for a deterministic candidate-ranking system.

The candidate ranking and match scores have already been calculated by the system.

Your job is ONLY to explain the provided ranking.

STRICT RULES:

1. Do NOT reorder candidates.
2. Do NOT create your own ranking.
3. Do NOT calculate or modify match scores.
4. Do NOT introduce skills, experience, projects, or qualifications that are not explicitly present in the provided evidence.
5. Use the evidence provided by the system as the source of truth.
6. If evidence is insufficient to support a claim, say that the evidence does not establish it.
7. Explain why each candidate ranks where they do.
8. Clearly distinguish between matched evidence and missing requirements.

Job:
{job}

Candidates in deterministic ranking order:
{context}
        """
        )


def build_candidate_context(job,top_k:int=5)->str:

    candidates=retrieve_and_rank_candidates(
        job,
        top_k=top_k
    )

    context=[]

    for candidate in candidates:

        candidate_skills = json.loads(candidate["skills"] or "[]")
        candidate_experience = json.loads(candidate["experience"] or "[]")

        required_skills = parse_job_list(job.required_skills)

        preferred_skills = parse_job_list(job.preferred_skills)

        job_responsibilities = parse_job_list(job.responsibilities)

        skill_evidence = build_skill_evidence(candidate_skills,required_skills,preferred_skills,)

        experience_evidence = build_experience_evidence(candidate_experience,job_responsibilities,)

        project_evidence = build_project_evidence(json.loads(candidate["projects"] or "[]"),required_skills,preferred_skills)

        qualification_evidence = build_qualification_evidence(json.loads(candidate["education"] or "[]"),parse_job_list(job.qualifications)
)
        
        context.append(
            f"""

            Candidate Rank: {candidates.index(candidate) + 1}
            Candidate ID: {candidate["candidate_id"]}
            Name: {candidate["name"]}

            RAW CANDIDATE DATA:

            Skills:
            {candidate["skills"]}

            Experience:   
            {candidate["experience"]}

            Projects:
            {candidate["projects"]}

            Education:
            {candidate["education"]}

            GROUNDED EVIDENCE:

            Evidence - Skills:
            {skill_evidence}

            Evidence - Experience:
            {experience_evidence}

            Evidence - Projects:
            {project_evidence}

            Evidence - Qualifications:
            {qualification_evidence}

            DETERMINISTIC MATCH RESULTS:

            Match Score: {candidate["score"]}
            Project Score: {candidate["project_score"]}
            Experience Score: {candidate["experience_score"]}
            Required Skills Score: {candidate["required_skill_score"]}
            Preferred Skills Score: {candidate["preferred_skill_score"]}
            Qualification Score: {candidate["qualification_score"]}
            """
        )

    return "\n".join(context)

def generate_candidate_analysis(job,top_k:int=5)->str:

    context=build_candidate_context(
        job,
        top_k=top_k
    )

    job_text = f"""
    Title: {job.title}
    Required Skills: {job.required_skills}
    Preferred Skills: {job.preferred_skills}
    Experience: {job.experience_years}
    Qualifications: {job.qualifications}
    Responsibilities: {job.responsibilities}
    """

    messages=prompt.format_messages(
        job=job_text,
        context=context

    )

    response=llm.invoke(messages)

    return response.content



