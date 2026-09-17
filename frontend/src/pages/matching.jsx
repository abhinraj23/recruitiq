import { useState } from "react"

function Matching() {
  const [candidates, setCandidates] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [selectedCandidate, setSelectedCandidate] = useState(null)

  const findCandidates = async () => {
    setLoading(true)
    setError("")

    try {
      const response = await fetch("/api/jobs/1/search?top_k=5")

      if (!response.ok) {
        throw new Error("Unable to find candidates")
      }

      const data = await response.json()

      setCandidates(data)
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  if (selectedCandidate) {
  const skills = JSON.parse(selectedCandidate.skills || "[]")
  const experience = JSON.parse(selectedCandidate.experience || "[]")
  const projects = JSON.parse(selectedCandidate.projects || "[]")
  const education = JSON.parse(selectedCandidate.education || "[]")

  return (
    <div className="page">
      <button
        className="secondary-button"
        onClick={() => setSelectedCandidate(null)}
      >
        ← Back to Matching
      </button>

      <button className="primary-button"
      onClick={() => { window.dispatchEvent(new CustomEvent("openInterview", {
        detail: {
          jobId: 1,
          candidateId: selectedCandidate.candidate_id,
        },
      })
    )
  }}
>
  Generate Interview Questions
      </button>

      <div className="page-header">
        <p className="eyebrow">MATCH DETAILS</p>
        <h1>{selectedCandidate.name}</h1>
        <p className="subtitle">
          Detailed candidate match for Python / AI Developer
        </p>
      </div>

      <div className="match-detail-score">
  <div>
    <strong>{Math.round(selectedCandidate.score)}%</strong>
    <span>Overall Match</span>
  </div>

  <div className="match-breakdown">
    <div>
      <span>Required Skills</span>
      <strong>
        {Math.round(selectedCandidate.required_skill_score * 100)}%
      </strong>
    </div>

    <div>
      <span>Preferred Skills</span>
      <strong>
        {Math.round(selectedCandidate.preferred_skill_score * 100)}%
      </strong>
    </div>

    <div>
      <span>Relevant Experience</span>
      <strong>
        {Math.round(selectedCandidate.experience_score * 100)}%
      </strong>
    </div>

    <div>
      <span>Qualification</span>
      <strong>
        {Math.round(selectedCandidate.qualification_score * 100)}%
      </strong>
    </div>
  </div>
</div>

      <div className="detail-card">
        <h2>Skills</h2>

        <div className="skill-list">
          {skills.map((skill, index) => (
            <span key={index}>{skill}</span>
          ))}
        </div>
      </div>

      <div className="detail-card">
        <h2>Experience</h2>

        {experience.map((job, index) => (
          <div className="experience-item" key={index}>
            <h3>{job.role}</h3>
            <p>{job.company}</p>
            {job.years && <span>{job.years} years</span>}

            <ul>
              {job.responsibilities?.slice(0, 4).map((item, itemIndex) => (
                <li key={itemIndex}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="detail-card">
        <h2>Projects</h2>

        {projects.map((project, index) => (
          <div className="project-item" key={index}>
            <h3>{project.name}</h3>
            <p>{project.description}</p>
          </div>
        ))}
      </div>

      <div className="detail-card">
        <h2>Education</h2>

        {education.map((item, index) => (
          <div className="education-item" key={index}>
            <h3>{item.degree}</h3>
            <p>{item.field}</p>
            <span>
              {item.institution} · {item.graduation_year}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

  return (
    <div className="page">

      <div className="page-header">
        <div>
          <p className="eyebrow">CANDIDATE SEARCH</p>

          <h1>Find Candidates</h1>

          <p className="subtitle">
            Find candidates that match your job requirements.
          </p>
        </div>
      </div>

      <div className="matching-job">

        <div>
          <span className="job-status">ACTIVE JOB</span>

          <h2>Python / AI Developer</h2>

          <p>
            Job ID: #JOB-001
          </p>
        </div>

        <button
          className="primary-button"
          onClick={findCandidates}
          disabled={loading}
        >
          {loading ? "Finding Candidates..." : "Find Candidates"}
        </button>

      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {candidates.length > 0 && (
        <div className="matching-results">

          <div className="results-header">
            <div>
              <h2>Matching Candidates</h2>

              <p>
                {candidates.length} candidates found
              </p>
            </div>
          </div>

          <div className="match-list">

            {candidates.map((candidate, index) => {

              const skills = JSON.parse(candidate.skills || "[]")

              const experience = JSON.parse(
                candidate.experience || "[]"
              )

              const projects = JSON.parse(
                candidate.projects || "[]"
              )

              return (
                <div
                  className="match-card"
                  key={candidate.candidate_id}
                >

                  <div className="match-card-header">

                    <div className="candidate-avatar">
                      {candidate.name.charAt(0)}
                    </div>

                    <div className="match-name">
                      <span className="rank">
                        #{index + 1}
                      </span>

                      <h2>{candidate.name}</h2>

                      <p>
                        {experience[0]?.role ||
                          "Candidate"}
                      </p>
                    </div>

                    <div className="match-score">
                      <strong>
                        {Math.round(candidate.score)}%
                      </strong>

                      <span>Match</span>
                    </div>

                  </div>


                  <div className="match-section">

                    <h3>Skills</h3>

                    <div className="skill-list">

                      {skills.slice(0, 8).map(
                        (skill, skillIndex) => (
                          <span key={skillIndex}>
                            {skill}
                          </span>
                        )
                      )}

                    </div>

                  </div>


                  <div className="match-summary">

                    <div>
                      <span>Experience</span>

                      <strong>
                        {experience.length > 0
                          ? `${experience.length} role${experience.length > 1 ? "s" : ""}`
                          : "Not available"}
                      </strong>
                    </div>

                    <div>
                      <span>Projects</span>

                      <strong>
                        {projects.length}
                      </strong>
                    </div>

                    <div>
                      <span>Qualification</span>

                      <strong>
                        {Math.round(
                          candidate.qualification_score * 100
                        )}%
                      </strong>
                    </div>

                  </div>


                  <button className="details-button"
                    onClick={() => {
                      setSelectedCandidate(candidate)
                    }}>
                      View Match Details →
                  </button>

                </div>
              )
            })
}
          </div>

        </div>
      )}

    </div>
  )
}

export default Matching