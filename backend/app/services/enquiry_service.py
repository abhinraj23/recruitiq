from app.services.vector_store import search_candidates
from app.services.evidence_service import build_enquiry_evidence
from sqlmodel import Session,select

from app.db.database import engine
from app.models.candidate import Candidate

from langchain_core.prompts import ChatPromptTemplate

from app.services.rag_service import llm

import json

from typing import Literal

from pydantic import BaseModel, Field

from app.services.evidence_service import (
    build_skill_evidence,
    build_experience_evidence,
    build_project_evidence,
    build_qualification_evidence,
)
from app.services.matcher import parse_job_list

class EnquiryQuery(BaseModel):
    intent: Literal[
        "candidate_search",
        "candidate_projects",
        "candidate_experience",
        "candidate_education",
        "candidate_details",
    ]
    search_terms: list[str] = Field(default_factory=list)
    candidate_name: str | None = None

query_prompt = ChatPromptTemplate.from_template(
"""
You are the query understanding component of RecruitIQ.

Convert the user's enquiry into a structured query.

Possible intents:

- candidate_search
- candidate_projects
- candidate_experience
- candidate_education
- candidate_details

Rules:

1. Extract the core concept, skill, technology, or topic being searched for.
2. Do not include surrounding question words such as "experience",
   "worked with", "worked on", "building", "candidates", or "which".
3. For experience-related questions, use the intent "candidate_experience"
   and extract the core experience/topic.
4. For project-related questions, use the intent "candidate_projects"
   and extract the relevant technology or project topic.
5. Do not invent skills, technologies, companies, or requirements.
6. If a specific candidate is mentioned, extract their name.
7. Return only the structured fields required by the schema.

User question:
{question}
"""
)

def understand_enquiry(
    question: str,
) -> EnquiryQuery:

    
    structured_llm = llm.with_structured_output(
        EnquiryQuery
    )


    messages = query_prompt.format_messages(
        question=question,
    )

    return structured_llm.invoke(
        messages
    )

def find_candidates_by_name(
    candidate_name: str,
    candidates,
) -> list:

    name = candidate_name.strip().lower()

    exact_matches = [
        candidate
        for candidate in candidates
        if candidate.name
        and candidate.name.strip().lower() == name
    ]

    return exact_matches


def search_candidates_structured(
    query: EnquiryQuery,
    candidates,
) -> list:

    if query.candidate_name:
        candidates = find_candidates_by_name(
            query.candidate_name,
            candidates,
        )

    if not query.search_terms:
        return candidates

    search_terms = [
        term.strip().lower()
        for term in query.search_terms
    ]

    matched_candidates = []

    for candidate in candidates:

        skills = json.loads(
            candidate.skills or "[]"
        )

        projects = json.loads(
            candidate.projects or "[]"
        )

        experience = json.loads(
            candidate.experience or "[]"
        )

        skill_text = " ".join(
            str(skill).lower()
            for skill in skills
        )

        project_text = " ".join(
            str(technology).lower()
            for project in projects
            for technology in project.get(
                "technologies",
                [],
            )
        )

        experience_text = " ".join(
            str(responsibility).lower()
            for experience_item in experience
            for responsibility in experience_item.get(
                "responsibilities",
                [],
            )
        )

        searchable_text = " ".join([
            skill_text,
            project_text,
            experience_text,
        ])

        if all(
            term in searchable_text
            for term in search_terms
        ):
            matched_candidates.append(candidate)

    return matched_candidates

def retrieve_enquiry_candidates(
    question: str,
    top_k: int = 5,
):
    results = search_candidates(
        question,
        top_k=top_k,
    )

    candidate_ids = results["ids"][0]

    candidates = []

    with Session(engine) as session:
        for candidate_id in candidate_ids:

            candidate = session.get(
                Candidate,
                int(candidate_id),
            )

            if not candidate:
                continue

            candidates.append(candidate)

    return candidates


def build_enquiry_context(
    candidates,
    search_terms: list[str] | None = None,
) -> str:

    context = []

    for candidate in candidates:

        candidate_context = f"""
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
""".strip()

        if search_terms:
            evidence = build_enquiry_evidence(
                candidate,
                search_terms,
            )

            candidate_context += f"""

ENQUIRY EVIDENCE:
{json.dumps(evidence, indent=2)}
"""

        context.append(candidate_context)

    return "\n\n---\n\n".join(context)


def retrieve_enquiry_context(
    question: str,
    top_k: int = 5,
) -> str:

    candidates = retrieve_enquiry_candidates(
        question,
        top_k=top_k,
    )

    return build_enquiry_context(candidates)


enquiry_prompt = ChatPromptTemplate.from_template(
"""
You are an enquiry assistant for RecruitIQ.

Answer the user's question using ONLY the candidate information
provided in the context.

STRICT RULES:

1. Do not invent candidate information.
2. Do not assume information that is not present in the context.
3. If the context does not contain enough information to answer,
   clearly say that the available data does not provide enough evidence.
4. Mention candidate names when answering candidate-related questions.
5. Keep the answer concise and directly answer the user's question.
6. Do not create scores or rankings unless they are explicitly
   provided in the context.

User question:
{question}

Candidate context:
{context}
"""
)


def generate_enquiry_answer(
    question: str,
    top_k: int = 5,
) -> str:

    query = understand_enquiry(question)

    route = route_enquiry(query)

    if route == "structured":

        candidates = retrieve_structured_candidates(
            query
        )

    else:

        candidates = retrieve_enquiry_candidates(
            question,
            top_k=top_k,
        )

    context = build_enquiry_context(
        candidates,
        search_terms=query.search_terms,
    )

    messages = enquiry_prompt.format_messages(
        question=question,
        context=context,
    )

    response = llm.invoke(messages)

    return response.content

def retrieve_structured_candidates(
    query: EnquiryQuery,
) -> list:

    with Session(engine) as session:
        candidates = session.exec(
            select(Candidate)
        ).all()

    return search_candidates_structured(
        query,
        candidates,
    )

def route_enquiry(
    query: EnquiryQuery,
) -> str:

    if query.candidate_name:
        return "structured"

    if query.intent in [
        "candidate_projects",
        "candidate_education",
        "candidate_details",
    ]:
        return "structured"

    if query.intent == "candidate_search" and query.search_terms:
        return "structured"

    return "semantic"