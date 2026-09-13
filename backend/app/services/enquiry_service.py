from app.services.evidence_service import build_enquiry_evidence
from app.services.matcher import parse_job_list, get_embeddings

from sklearn.metrics.pairwise import cosine_similarity
from sqlmodel import Session,select

from app.db.database import engine
from app.models.candidate import Candidate

from langchain_core.prompts import ChatPromptTemplate

from app.services.rag_service import llm

import json

from typing import Literal

from pydantic import BaseModel, Field


class EnquiryQuery(BaseModel):
    intent: Literal[
        "candidate_search",
        "candidate_projects",
        "candidate_experience",
        "candidate_education",
        "candidate_details",
    ]
    retrieval_mode: Literal["structured", "semantic"]
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

Possible retrieval modes:

- structured
- semantic

Use STRUCTURED retrieval when:
- The user asks for an exact candidate, field, or known attribute.
- The user names a specific candidate.
- The user asks for an exact skill, technology, qualification, or project technology.
- The requested information can be found through direct matching in candidate data.

Use SEMANTIC retrieval when:
- The user asks about a concept, capability, similarity, or type of work.
- The exact wording may not appear in the candidate data.
- The user asks whether candidates have done something similar to the described activity.
- The question requires understanding the meaning of projects or experience rather than matching an exact field or term.

Examples:

"Tell me about Karthik Menon's projects."
→ intent: candidate_projects
→ retrieval_mode: structured
→ candidate_name: "Karthik Menon"

"Which candidates have projects using AWS S3?"
→ intent: candidate_projects
→ retrieval_mode: structured
→ search_terms: ["AWS S3"]

"Which candidates have built projects related to retail sales?"
→ intent: candidate_projects
→ retrieval_mode: semantic
→ search_terms: ["retail sales"]

"Which candidates have experience building data pipelines?"
→ intent: candidate_experience
→ retrieval_mode: semantic
→ search_terms: ["data pipelines"]

"Which candidates have worked with AWS?"
→ intent: candidate_search
→ retrieval_mode: structured
→ search_terms: ["AWS"]

Rules:

1. Extract the core concept, skill, technology, or topic being searched for.
2. Do not include surrounding question words such as "experience",
   "worked with", "worked on", "candidates", or "which".
3. Do not invent skills, technologies, companies, or requirements.
4. If a specific candidate is mentioned, extract their name.
5. Choose the retrieval mode based on HOW the information needs to be found,
   not simply on the intent.
6. Return only the structured fields required by the schema.
7. For exact education/qualification queries, extract the normalized
   qualification level when appropriate.

Examples:

For education queries:

- Use STRUCTURED retrieval for:
  - exact degree or degree level
  - graduation year
  - institution
  - a specific candidate's education

- Use SEMANTIC retrieval for:
  - academic background related to a concept
  - fields of study related to a topic
  - educational background similar to a described area

Examples:

"Which candidates have an academic background related to artificial intelligence?"
→ intent: candidate_education
→ retrieval_mode: semantic
→ search_terms: ["artificial intelligence"]

"Which candidates studied a field related to data science?"
→ intent: candidate_education
→ retrieval_mode: semantic
→ search_terms: ["data science"]

"What degree does Karthik Menon have?"
→ intent: candidate_education
→ retrieval_mode: structured
→ candidate_name: "Karthik Menon"

"Which candidates have a bachelor's degree?"
→ intent: candidate_education
→ retrieval_mode: structured
→ search_terms: ["bachelor"]

"Which candidates have a master's degree?"
→ intent: candidate_education
→ retrieval_mode: structured
→ search_terms: ["master"]

"Which candidates have a PhD?"
→ intent: candidate_education
→ retrieval_mode: structured
→ search_terms: ["phd"]

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

        education = json.loads(
            candidate.education or "[]"
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

        education_levels = {
            item.get("degree_level", "").lower()
            for item in education
        }

        if query.intent == "candidate_education":

            matches = all(
                term in education_levels
                for term in search_terms
            )

        else:

            searchable_text = " ".join([
                skill_text,
                project_text,
                experience_text,
            ])

            matches = all(
                term in searchable_text
                for term in search_terms
            )

        if matches:
            matched_candidates.append(candidate)

    return matched_candidates



def build_enquiry_context(
    candidates,
    search_terms: list[str] | None = None,
    semantic_evidence: dict | None = None,
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
        if semantic_evidence and candidate.id in semantic_evidence:
            candidate_context += f"""

SEMANTIC EVIDENCE:
{json.dumps(
    semantic_evidence[candidate.id],
    indent=2
)}
"""

        context.append(candidate_context)

    return "\n\n---\n\n".join(context)





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

def semantic_project_search(
    search_terms: list[str],
    candidates,
    threshold: float = 0.65
) -> list:
    if not search_terms:
        return []

    query_text = " ".join(search_terms).strip()

    project_texts = []
    project_owners = []

    for candidate in candidates:
        projects = json.loads(candidate.projects or "[]")

        for project in projects:
            project_text = " ".join([
                str(project.get("name", "")),
                str(project.get("description", "")),
                " ".join(str(tech) for tech in project.get("technologies", [])),
            ]).strip()

            if project_text:
                project_texts.append(project_text)
                project_owners.append(candidate)

    if not project_texts:
        return []

    embeddings = get_embeddings([query_text] + project_texts)

    query_embedding = embeddings[0]
    project_embeddings = embeddings[1:]

    similarities = cosine_similarity(
        [query_embedding],
        project_embeddings,
    )[0]

    matched_candidates = []
    seen_candidate_ids = set()

    for index, similarity in enumerate(similarities):
        if similarity >= threshold:
            candidate = project_owners[index]

            if candidate.id not in seen_candidate_ids:
                matched_candidates.append(candidate)
                seen_candidate_ids.add(candidate.id)

    return matched_candidates


def semantic_experience_search(
    search_terms: list[str],
    candidates,
    threshold: float = 0.65
) -> list:
    if not search_terms:
        return []

    query_text = " ".join(search_terms).strip()

    experience_texts = []
    experience_owners = []
    experience_details = []

    for candidate in candidates:
        experiences = json.loads(candidate.experience or "[]")

        for experience in experiences:
            responsibilities = experience.get("responsibilities", [])

            experience_text = " ".join(
                str(responsibility)
                for responsibility in responsibilities
            ).strip()

            if experience_text:
                experience_texts.append(experience_text)
                experience_owners.append(candidate)
                experience_details.append({
                    "role": experience.get("role", ""),
                    "company": experience.get("company", ""),
                    "responsibilities": responsibilities,
                })

    if not experience_texts:
        return []

    embeddings = get_embeddings(
        [query_text] + experience_texts
    )

    query_embedding = embeddings[0]
    experience_embeddings = embeddings[1:]

    similarities = cosine_similarity(
        [query_embedding],
        experience_embeddings,
    )[0]

    matched_candidates = {}
    
    for index, similarity in enumerate(similarities):
        similarity = float(similarity)

        if similarity >= threshold:
            candidate = experience_owners[index]

            if candidate.id not in matched_candidates:
                matched_candidates[candidate.id] = {
                    "candidate": candidate,
                    "evidence": [],
                }

            matched_candidates[candidate.id]["evidence"].append({
                "role": experience_details[index]["role"],
                "company": experience_details[index]["company"],
                "responsibilities": experience_details[index]["responsibilities"],
                "similarity": round(similarity, 3),
            })

    return list(matched_candidates.values())


def semantic_education_search(
    search_terms: list[str],
    candidates,
    threshold: float = 0.65
) -> list:
    if not search_terms:
        return []

    query_text = " ".join(search_terms).strip()

    education_texts = []
    education_owners = []
    education_details = []

    for candidate in candidates:
        education = json.loads(candidate.education or "[]")

        for education_item in education:
            education_text = " ".join([
                str(education_item.get("degree", "")),
                str(education_item.get("degree_level", "")),
                str(education_item.get("field", "")),
                str(education_item.get("institution", "")),
            ]).strip()

            if education_text:
                education_texts.append(education_text)
                education_owners.append(candidate)
                education_details.append(education_item)

    if not education_texts:
        return []

    embeddings = get_embeddings(
        [query_text] + education_texts
    )

    query_embedding = embeddings[0]
    education_embeddings = embeddings[1:]

    similarities = cosine_similarity(
        [query_embedding],
        education_embeddings,
    )[0]

    matched_candidates = {}

    for index, similarity in enumerate(similarities):
        similarity = float(similarity)

        if similarity >= threshold:
            candidate = education_owners[index]

            if candidate.id not in matched_candidates:
                matched_candidates[candidate.id] = {
                    "candidate": candidate,
                    "evidence": [],
                }

            matched_candidates[candidate.id]["evidence"].append({
                "degree": education_details[index].get("degree", ""),
                "degree_level": education_details[index].get("degree_level", ""),
                "field": education_details[index].get("field", ""),
                "institution": education_details[index].get("institution", ""),
                "graduation_year": education_details[index].get("graduation_year"),
                "similarity": round(similarity, 3),
            })

    return list(matched_candidates.values())

def generate_enquiry_answer(
    question: str,
    top_k: int = 5,
) -> str:

    query = understand_enquiry(question)

    semantic_evidence = None

    route = route_enquiry(query)

    if route == "structured":

        candidates = retrieve_structured_candidates(
            query
        )

    elif query.intent == "candidate_projects":

        with Session(engine) as session:
            all_candidates = session.exec(select(Candidate)).all()

            candidates = semantic_project_search(search_terms=query.search_terms,candidates=all_candidates)

            candidates = candidates[:top_k]

    elif query.intent == "candidate_experience":

        with Session(engine) as session:
            all_candidates = session.exec(select(Candidate)).all()

        experience_results = semantic_experience_search(search_terms=query.search_terms,candidates=all_candidates,)

        experience_results = experience_results[:top_k]

        semantic_evidence = {result["candidate"].id: result["evidence"] for result in experience_results}

        candidates = [result["candidate"] for result in experience_results]

    elif query.intent == "candidate_education":

        with Session(engine) as session:
            all_candidates = session.exec(select(Candidate)).all()

        education_results = semantic_education_search(search_terms=query.search_terms,candidates=all_candidates,)

        education_results = education_results[:top_k]

        semantic_evidence = {result["candidate"].id: result["evidence"] for result in education_results}

        candidates = [result["candidate"] for result in education_results]

    else:
        raise ValueError(f"Unsupported enquiry intent: {query.intent}")

    context = build_enquiry_context(
        candidates,
        search_terms=query.search_terms,
        semantic_evidence=semantic_evidence,
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

    return query.retrieval_mode