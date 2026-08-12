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
    
    candidate_tech=set()

    for project in candidate_projects:
        for tech in project.get("technologies",[]):
            candidate_tech.add(normalize(tech))

    required={normalize(skill) for skill in required_tech}

    matched=candidate_tech.intersection(required)

    return len(matched)/len(required)


def experience_match(candidate_experience:list[dict],job_role:str,required_years:float|None,job_responsibilities:list[str])->float:
    if not candidate_experience:
        return 0.0
    
    target_role=normalize(job_role)
    total_duties=len(job_responsibilities)

    relevant_years=0.0
    responsibility_matches=0

    for experience in candidate_experience:
        role=normalize(experience.get("role",""))

        if role in target_role or target_role in role:
            relevant_years+=experience.get("years",0) or 0

            candidate_responsibilities=[normalize(responsibility) for responsibility in experience.get("responsibilities",[])]

            for duty in job_responsibilities:
                duty=normalize(duty)

                if any(duty in candidate_duty or candidate_duty in duty for candidate_duty in candidate_responsibilities):
                    responsibility_matches+=1 
                
    
    if required_years:
        duration_score=min(relevant_years/required_years,1.0)
    else:
        duration_score=1.0

    
    if total_duties:
        duties_score=responsibility_matches/total_duties
    else:
        duties_score=1.0
    

    return (
        duties_score*0.3+duration_score*0.7
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

    return 1.0



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

    experience_score=experience_match(candidate_experiece,job.title,job.experience_years,job_responsibilities)

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




