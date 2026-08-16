import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


semantic_model=SentenceTransformer("BAAI/bge-small-en-v1.5")


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

    project_descriptions = []


    for project in candidate_projects:
        technologies={normalize(tech) for tech in project.get("technologies",[])}

        matched.update(technologies.intersection(required))

        description=normalize(project.get("description",[]))

        if description:
            project_descriptions.append(description)

        for tech in required:
            if tech in description:
                matched.add(tech)
        
    lexical_score=len(matched)/len(required)

    if not project_descriptions:
        return lexical_score
    
    
    required_list=list(required)
    required_embedding=semantic_model.encode(required_list)

    projects_embedding=semantic_model.encode(project_descriptions)

    similarity_matrix = cosine_similarity(
        required_embedding,
        projects_embedding
    )

    semantic_scores=[]

    semantic_threshold=0.65

    for index,tech in enumerate(required_list):
        if tech in matched:
            semantic_scores.append(1.0)
            continue
        
        best_similarity = float(
            similarity_matrix[index].max()
        )

        if best_similarity >= semantic_threshold:
            semantic_scores.append(best_similarity)
        else:
            semantic_scores.append(0.0)
    
    semantic_score = (
        sum(semantic_scores) / len(semantic_scores)
    )



    return (lexical_score*0.7+semantic_score*0.3)




def experience_match(candidate_experience:list[dict],required_years:float|None,job_required_skills:list[str],job_preferred_skills:list[str],job_responsibilities:list[str])->float:
    if not candidate_experience:
        return 0.0
    
    if not job_required_skills and not job_preferred_skills:
        return 0.0
    

    relevant_years=0.0
    experience_relevance_score=[]

    threshold=0.30

    jd_embedding=semantic_model.encode(job_responsibilities)

    for experience in candidate_experience:

        candidate_responsibilities=[normalize(responsibility) for responsibility in experience.get("responsibilities",[])]

        if not candidate_responsibilities:
            continue
        
        candidate_text=" ".join(candidate_responsibilities)
        
        matched_required ={
            normalize(skill) for skill in job_required_skills if normalize(skill) in candidate_text 
        }

        matched_preferred={
            normalize(skill) for skill in job_preferred_skills if normalize(skill) in candidate_text
        }

        required_score=(len(matched_required)/len(job_required_skills) if matched_required else 0.0)

        preferred_score=(len(matched_preferred)/len(job_preferred_skills) if matched_preferred else 0.0)

        lexical_score=(required_score*0.7+preferred_score*0.3)

        #semantic processing

        candidate_embedding=semantic_model.encode(job_responsibilities)

        similarity_matrix=cosine_similarity(
            candidate_embedding,jd_embedding
        )

        semantic_score=float(similarity_matrix.max())

        relevance_score=(lexical_score*0.6+semantic_score*0.4)

        experience_relevance_score.append(relevance_score)


        if relevance_score>=threshold:
            relevant_years+=(experience.get("years",0) or 0)
    
    if not experience_relevance_score:
        return 0.0
    

    relevance_score=max(experience_relevance_score)

    if required_years:

        duration_score=min(relevant_years/required_years,1.0)

    else:
        duration_score=1.0
    

    return (
        relevance_score*0.3+duration_score*0.7
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
    
    requested_fields = []

    for terms in field_groups.values():
        for term in terms:
            if term in job_text:
                requested_fields.append(term)
    
    if not requested_fields:
        requested_fields=[]
    
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
        if any(
            term in degree
            for term in [
                "phd",
                "ph.d",
                "doctorate",
                "doctoral",
            ]
        ):
            candidate_level = "phd"

        elif any(
            term in degree
            for term in [
                "master",
                "m.tech",
                "mtech",
                "m.e",
                "m.sc",
                "msc",
            ]
        ):
            candidate_level = "master"

        elif any(
            term in degree
            for term in [
                "bachelor",
                "b.tech",
                "btech",
                "b.e",
                "b.sc",
                "bsc",
            ]
        ):
            candidate_level = "bachelor"

        else:
            candidate_level = None

        degree_rank = {
            "bachelor": 1,
            "master": 2,
            "phd": 3,
        }

        
        if required_level:

            if candidate_level not in degree_rank:
                continue

            if (
                degree_rank[candidate_level]
                < degree_rank[required_level]
            ):
                continue

        if not requested_fields:
            best_score = max(best_score, 1.0)
            continue
        
        candidate_groups = set()

        for group, terms in field_groups.items():
            if any(
                term in candidate_text
                for term in terms
            ):
                candidate_groups.add(group)

        requested_groups = set()

        for group, terms in field_groups.items():
            if any(
                term in job_text
                for term in terms
            ):
                requested_groups.add(group)

        if requested_groups.intersection(
            candidate_groups
        ):
            lexical_score = 1.0

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
            lexical_score = 0.5

        else:
            lexical_score = 0.0

        #semantic processing
        
        candidate_field = field

        if candidate_field and requested_fields:

            requested_embeddings = semantic_model.encode(
                requested_fields
            )

            candidate_embedding = semantic_model.encode(
                [candidate_field]
            )

            similarity_matrix = cosine_similarity(
                requested_embeddings,
                candidate_embedding
            )

            semantic_score = float(
                similarity_matrix.max()
            )

        else:
            semantic_score = 0.0
        
        field_score = (
            lexical_score * 0.7
            + semantic_score * 0.3
        )

        best_score = max(
            best_score,
            field_score
        )

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

    experience_score=experience_match(candidate_experiece,job.experience_years,job_required_skills,job_preferred_skills,job_responsibilities)

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




