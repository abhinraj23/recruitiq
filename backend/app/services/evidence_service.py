from app.services.matcher import (normalize,get_embeddings)

from sklearn.metrics.pairwise import cosine_similarity
import json

def build_skill_evidence(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> dict:

    candidate = {
        normalize(skill)
        for skill in candidate_skills
    }

    required = {
        normalize(skill)
        for skill in required_skills
    }

    preferred = {
        normalize(skill)
        for skill in preferred_skills
    }

    matched_required = sorted(
        candidate.intersection(required)
    )

    missing_required = sorted(
        required.difference(candidate)
    )

    matched_preferred = sorted(
        candidate.intersection(preferred)
    )

    missing_preferred = sorted(
        preferred.difference(candidate)
    )

    return {
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
    }


def build_experience_evidence(
    candidate_experience: list[dict],
    job_responsibilities: list[str],
) -> dict:

    evidence = []

    if not candidate_experience or not job_responsibilities:
        return {
            "relevant_experience": [],
        }

    candidate_responsibilities = []

    for experience in candidate_experience:
        for responsibility in experience.get("responsibilities", []):
            candidate_responsibilities.append({
                "role": experience.get("role", ""),
                "company": experience.get("company", ""),
                "responsibility": responsibility,
            })

    candidate_texts = [
        normalize(item["responsibility"])
        for item in candidate_responsibilities
    ]

    job_texts = [
        normalize(responsibility)
        for responsibility in job_responsibilities
    ]

    embeddings = get_embeddings(
        candidate_texts + job_texts
    )

    candidate_embeddings = embeddings[:len(candidate_texts)]
    job_embeddings = embeddings[len(candidate_texts):]

    similarity_matrix = cosine_similarity(
        candidate_embeddings,
        job_embeddings
    )

    threshold = 0.65

    for index, item in enumerate(candidate_responsibilities):

        best_job_index = similarity_matrix[index].argmax()

        best_similarity = float(
            similarity_matrix[index][best_job_index]
        )

        if best_similarity >= threshold:
            evidence.append({
                "role": item["role"],
                "company": item["company"],
                "responsibility": item["responsibility"],
                "matched_job_responsibility": job_responsibilities[best_job_index],
                "similarity": round(best_similarity, 3),
            })

    return {
        "relevant_experience": evidence,
    }


def build_project_evidence(
    candidate_projects: list[dict],
    job_required_skills: list[str],
    preferred_skills: list[str],
) -> dict:

    evidence = []

    if not candidate_projects or not job_required_skills:
        return {
            "relevant_projects": [],
        }

    required = {
        normalize(skill)
        for skill in job_required_skills
    }

    preferred = {
        normalize(skill)
        for skill in preferred_skills
    }

    for project in candidate_projects:

        technologies = {
            normalize(tech)
            for tech in project.get("technologies", [])
        }

        matched_required = sorted(
            technologies.intersection(required)
        )

        matched_preferred = sorted(
            technologies.intersection(preferred)
        )


        if matched_required or matched_preferred:
            evidence.append({
                "title": project.get("title", ""),
                "description": project.get("description", ""),
                "technologies": project.get("technologies", []),
                "matched_required_skills": matched_required,
                "matched_preferred_skills": matched_preferred,
            })

    return {
        "relevant_projects": evidence,
    }


def build_qualification_evidence(
    candidate_education: list[dict],
    job_qualifications: list[str],
) -> dict:

    if not candidate_education or not job_qualifications:
        return {
            "qualification_evidence": {}
        }

    return {
        "qualification_evidence": {
            "job_requirement": job_qualifications,
            "candidate_education": candidate_education,
        }
    }

def build_enquiry_evidence(
    candidate,
    search_terms: list[str],
) -> dict:

    skills = json.loads(
        candidate.skills or "[]"
    )

    projects = json.loads(
        candidate.projects or "[]"
    )

    experience = json.loads(
        candidate.experience or "[]"
    )

    evidence = {}

    for search_term in search_terms:

        term = normalize(search_term)

        term_evidence = {
            "skills": [],
            "projects": [],
            "experience": [],
        }

        # Skills
        for skill in skills:
            if term in normalize(skill):
                term_evidence["skills"].append(skill)

        # Projects
        for project in projects:
            matched_technologies = [
                technology
                for technology in project.get(
                    "technologies",
                    []
                )
                if term in normalize(technology)
            ]

            if matched_technologies:
                term_evidence["projects"].append({
                    "title": project.get("title", ""),
                    "technologies": matched_technologies,
                })

        # Experience
        for experience_item in experience:
            matched_responsibilities = [
                responsibility
                for responsibility in experience_item.get(
                    "responsibilities",
                    []
                )
                if term in normalize(responsibility)
            ]

            if matched_responsibilities:
                term_evidence["experience"].append({
                    "role": experience_item.get("role", ""),
                    "company": experience_item.get("company", ""),
                    "responsibilities": matched_responsibilities,
                })

        # Only include terms for which we actually found evidence
        if any(term_evidence.values()):
            evidence[search_term] = term_evidence

    return {
        "candidate_id": candidate.id,
        "candidate_name": candidate.name,
        "evidence": evidence,
    }