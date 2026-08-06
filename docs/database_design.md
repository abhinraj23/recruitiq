# RecruitIQ Database Design

## Overview

RecruitIQ is built around a recruiter-centric workflow. Every piece of data belongs to a user and is linked together through relationships.

---

## Entity: User

Represents a registered recruiter using RecruitIQ.

| Field | Description |
|--------|-------------|
| id | Unique user ID |
| name | Full name |
| email | User email |
| password_hash | Hashed password |
| created_at | Account creation timestamp |

---

## Entity: Job

Represents a job opening uploaded by a recruiter.

| Field | Description |
|--------|-------------|
| id | Unique job ID |
| user_id | Owner of the job |
| title | Job title |
| company | Company name |
| description | Original job description |
| extracted_skills | AI extracted skills |
| created_at | Upload timestamp |

---

## Entity: Candidate

Represents a candidate profile.

| Field | Description |
|--------|-------------|
| id | Unique candidate ID |
| user_id | Owner of the candidate |
| name | Candidate name |
| email | Candidate email |
| phone | Candidate phone |
| parsed_data | Structured resume JSON |
| created_at | Upload timestamp |

---

## Entity: ResumeDocument

Stores the uploaded resume file.

| Field | Description |
|--------|-------------|
| id | Unique document ID |
| candidate_id | Related candidate |
| file_name | Original filename |
| extracted_text | Parsed resume text |
| embedding_status | Pending / Completed |
| uploaded_at | Upload timestamp |

---

## Entity: Match

Stores AI matching results between a candidate and a job.

| Field | Description |
|--------|-------------|
| id | Unique match ID |
| candidate_id | Candidate |
| job_id | Job |
| score | Match score |
| explanation | AI reasoning |
| created_at | Match timestamp |

---

## Entity: Conversation

Represents one recruiter chat session.

| Field | Description |
|--------|-------------|
| id | Conversation ID |
| user_id | Owner |
| job_id | Optional related job |
| title | Conversation title |
| created_at | Created timestamp |

---

## Entity: Message

Stores every chat message.

| Field | Description |
|--------|-------------|
| id | Message ID |
| conversation_id | Parent conversation |
| role | user / assistant / system |
| content | Message text |
| citations | Retrieved document sources |
| created_at | Timestamp |

---

# Relationships

User
├── Jobs
├── Candidates
├── Conversations
│
Job
├── Matches
│
Candidate
├── ResumeDocument
├── Matches
│
Conversation
└── Messages