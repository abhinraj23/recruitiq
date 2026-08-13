import json


def normalize(sample:str)->str:
    return sample.strip().lower()


def skill_match(candidate_skills:list[str],required_skills:list[str])->float:
    if not required_skills:
        return 1.0
    
    candidate={normalize(skill) for skill in candidate_skills}
    required={normalize(skill) for skill in required_skills}

    matched=candidate.intersection(required)

    return len(matched)/len(required)


def project_match(candidate_projects:list[dict],required_tech:list[str])->float:
    if not required_tech:
        return 1.0
    
    required={normalize(skill) for skill in required_tech}
    matched=set()

    for project in candidate_projects:
        technologies={normalize(tech) for tech in project.get("technologies",[])}

        matched.update(technologies.intersection(required))

        description=normalize(project.get("description",[]))

        for tech in required:
            if tech in description:
                matched.add(tech)
        
    return len(matched)/len(required)



def experience_match(candidate_experience:list[dict],required_years:float|None,job_required_skills:list[str],job_preferred_skills:list[str])->float:
    if not candidate_experience:
        return 0.0
    
    if not job_required_skills and not job_preferred_skills:
        return 0.0
    

    relevant_years=0.0
    experience_relevance_score=[]

    threshold=0.30

    for experience in candidate_experience:

        candidate_responsibilities=",".join(normalize(responsibility) for responsibility in experience.get("responsibilities",[]))

        if not candidate_responsibilities:
            continue
        
        matched_required ={
            normalize(skill) for skill in job_required_skills if normalize(skill) in candidate_responsibilities 
        }

        matched_preferred={
            normalize(skill) for skill in job_preferred_skills if normalize(skill) in candidate_responsibilities
        }

        required_score=(len(matched_required)/len(job_required_skills) if matched_required else 0.0)

        preferred_score=(len(matched_preferred)/len(job_preferred_skills) if matched_preferred else 0.0)

        relavance_score=(required_score*0.7+preferred_score*0.3)

        experience_relevance_score.append(relavance_score)

        if relavance_score>=threshold:
            relevant_years+=(experience.get("years",0) or 0)
    
    if not experience_relevance_score:
        return 0.0
    

    relavance_score=max(experience_relevance_score)

    if required_years:

        duration_score=min(relevant_years/required_years,1.0)

    else:
        duration_score=1.0
    

    return (
        relavance_score*0.3+duration_score*0.7
    )



def preferred_skill_match(candidate_skills:list[str],job_skills:list[str])->float:
    if not job_skills:
        return 1.0

    candidate={normalize(skill) for skill in candidate_skills}
    required={normalize(skill) for skill in job_skills}

    matched=candidate.intersection(required)

    return len(matched)/len(required)            



def qualification_match(
    candidate_education: list[dict],
    job_qualifications: list[str],
) -> float:

    if not job_qualifications:
        return 1.0

    if not candidate_education:
        return 0.0

    job_text = normalize(
        " ".join(str(item) for item in job_qualifications)
    )

    # Detect the required degree level from the JD
    if any(
        term in job_text
        for term in ["master","masters", "m.tech", "mtech", "m.e", "m.sc", "msc"]
    ):
        required_level = "master"

    elif any(
        term in job_text
        for term in [
            "bachelor",
            "b.tech",
            "btech",
            "b.e",
            "b.e.",
            "b.sc",
            "bsc",
        ]
    ):
        required_level = "bachelor"
    
    elif any(
    term in job_text
    for term in ["phd", "ph.d", "doctorate", "doctoral"]):
        required_level = "phd"

    else:
        required_level = None

    # Broad field groups used only to interpret the JD
    field_groups = {
        "computer": [
            "computer science",
            "computer engineering",
            "software engineering",
            "information technology",
            "information systems",
        ],
        "electronics": [
            "electronics",
            "electronics and communication",
            "ece",
            "eee",
            "electrical",
            "electrical and electronics"
        ],
        "data": [
            "data science",
            "data analytics",
            "statistics",
        ],
        "ai": [
            "artificial intelligence",
            "machine learning",
        ],
    }

    requested_groups = set()

    for group, terms in field_groups.items():
        if any(term in job_text for term in terms):
            requested_groups.add(group)

    best_score = 0.0

    for education in candidate_education:

        degree = normalize(
            str(education.get("degree", ""))
        )

        field = normalize(
            str(education.get("field", ""))
        )

        candidate_text = f"{degree} {field}"

        # Check degree level
        if required_level == "bachelor":
            degree_match = any(
                term in degree
                for term in [
                    "bachelor",
                    "b.tech",
                    "btech",
                    "b.e",
                    "b.sc",
                    "bsc",
                ]
            )

        elif required_level == "master":
            degree_match = any(
                term in degree
                for term in [
                    "master",
                    "m.tech",
                    "mtech",
                    "m.e",
                    "m.sc",
                    "msc",
                ]
            )
        
        elif required_level=="phd":
            degree_match=any(
                term in degree
                for term in [
                    "phd",
                    "ph.d",
                    "doctorate",
                    "doctoral"
                ]
            )
        

        else:
            degree_match = True

        if not degree_match:
            continue

        # If the JD doesn't specify a field,
        # matching the degree level is sufficient.
        if not requested_groups:
            best_score = max(best_score, 1.0)
            continue

        candidate_groups = set()

        for group, terms in field_groups.items():
            if any(term in candidate_text for term in terms):
                candidate_groups.add(group)

        # Correct degree + relevant field
        if requested_groups.intersection(candidate_groups):
            best_score = max(best_score, 1.0)

        # Correct degree but technical/related field
        elif any(
            term in candidate_text
            for term in [
                "engineering",
                "technology",
                "computer",
                "science",
                "information",
                "data",
            ]
        ):
            best_score = max(best_score, 0.5)

        # Correct degree but unrelated field
        else:
            best_score = max(best_score, 0.0)

    return best_score



def calculate_match_score(project_score:float,experience_score:float,required_skills_score:float,preferred_skills_score:float,qualification_score:float)->float:
    score=(
        project_score*0.30
        +experience_score*0.25
        +required_skills_score*0.25
        +preferred_skills_score*0.10
        +qualification_score*0.10
    )

    return round(score*100,2)


def candidate_to_job(candidate,job):
    candidate_projects=json.loads(candidate.projects or "[]")
    candidate_experiece=json.loads(candidate.experience or "[]")
    candidate_skills=json.loads(candidate.skills or "[]")
    candidate_education=json.loads(candidate.education or "[]")

    job_required_skills = [
        item.strip()
        for item in (job.required_skills or "").split(",")
        if item.strip()
    ]

    job_preferred_skills = [
        item.strip()
        for item in (job.preferred_skills or "").split(",")
        if item.strip()
    ]

    job_qualifications = [
        item.strip()
        for item in (job.qualifications or "").split(",")
        if item.strip()
    ]

    job_responsibilities= [
        item.strip()
        for item in (job.responsibilities or "").split(",")
        if item.strip()
    ]

    project_score=project_match(candidate_projects,job_required_skills)

    required_skill_score=skill_match(candidate_skills,job_required_skills)

    preferred_skill_score=preferred_skill_match(candidate_skills,job_preferred_skills)

    experience_score=experience_match(candidate_experiece,job.experience_years,job_required_skills,job_preferred_skills)

    qualification_score=qualification_match(candidate_education,job_qualifications)

    final_score=calculate_match_score(
        project_score,experience_score,required_skill_score,preferred_skill_score,qualification_score
    )

    return {
        "score": final_score,
        "project_score": project_score,
        "experience_score": experience_score,
        "required_skill_score": required_skill_score,
        "preferred_skill_score": preferred_skill_score,
        "qualification_score": qualification_score,
    }




