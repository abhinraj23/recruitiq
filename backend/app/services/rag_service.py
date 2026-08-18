import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.services.candidate_retrieval import retrieve_and_rank_candidates

load_dotenv()

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0

)

prompt=ChatPromptTemplate.from_template(
        """
        You are a recruiter assistant.

        Use ONLY the candidate information provided below.

        Job:
        {job}

        Candidate information:
        {context}

        Explain which candidates are strongest for this job and why.

        Do not invent candidate experience, skills, projects, or qualifications.
        """
        )


def build_candidate_context(job,top_k:int=5)->str:

    candidates=retrieve_and_rank_candidates(
        job,
        top_k=top_k
    )

    context=[]

    for candidate in candidates:
        
        context.append(
            f"""
            Candidate ID: {candidate["candidate_id"]}
            Name: {candidate["name"]}

            Skills:
            {candidate["skills"]}

            Experience:   
            {candidate["experience"]}

            Projects:
            {candidate["projects"]}

            Education:
            {candidate["education"]}

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



