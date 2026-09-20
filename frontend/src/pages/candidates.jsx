import { useEffect, useState } from "react"

function Candidates() {
  const [candidates, setCandidates] = useState([])
  const [search, setSearch] = useState("")
  const [selectedCandidate, setSelectedCandidate] = useState(null)

  useEffect(() => {
    fetch("/api/resumes/debug")
      .then((response) => response.json())
      .then((data) => {
        setCandidates(data.candidates)
      })
  }, [])

  const filteredCandidates = candidates.filter((candidate) =>
    candidate.name.toLowerCase().includes(search.toLowerCase())
  )

  // Show ONE candidate profile
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
          ← Back to Candidates
        </button>

        <div className="page-header">
          <p className="eyebrow">CANDIDATE PROFILE</p>

          <h1>{selectedCandidate.name}</h1>

          <p className="subtitle">
            Candidate #{selectedCandidate.id}
          </p>
        </div>

        <div className="detail-card">
          <h2>Contact</h2>

          <p>
            {selectedCandidate.email || "Email not available"}
          </p>

          <p>
            {selectedCandidate.phone || "Phone not available"}
          </p>
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

          {experience.length === 0 && (
            <p>No experience information available.</p>
          )}

          {experience.map((item, index) => (
            <div className="experience-item" key={index}>
              <h3>{item.role}</h3>

              <p>{item.company}</p>

              {item.years && (
                <span>{item.years} years</span>
              )}

              {item.responsibilities && (
                <ul>
                  {item.responsibilities
                    .slice(0, 4)
                    .map((responsibility, responsibilityIndex) => (
                      <li key={responsibilityIndex}>
                        {responsibility}
                      </li>
                    ))}
                </ul>
              )}
            </div>
          ))}
        </div>

        <div className="detail-card">
          <h2>Projects</h2>

          {projects.length === 0 && (
            <p>No project information available.</p>
          )}

          {projects.map((project, index) => (
            <div className="project-item" key={index}>
              <h3>{project.name}</h3>

              <p>{project.description}</p>
            </div>
          ))}
        </div>

        <div className="detail-card">
          <h2>Education</h2>

          {education.length === 0 && (
            <p>No education information available.</p>
          )}

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

  // Main candidates list
  return (
    <div className="page">
      <div className="page-header">
        <p className="eyebrow">TALENT</p>

        <h1>Candidates</h1>

        <p className="subtitle">
          Browse and search your candidate database.
        </p>
      </div>

      <div className="candidate-toolbar">
        <input
          type="text"
          placeholder="Search candidates..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />

        <span>
          {filteredCandidates.length} candidates
        </span>
      </div>

      <div className="candidate-grid">
        {filteredCandidates.map((candidate) => {
          const skills = JSON.parse(candidate.skills || "[]")

          return (
            <div
              className="candidate-card"
              key={candidate.id}
            >
              <div className="candidate-header">
                <div className="candidate-avatar">
                  {candidate.name.charAt(0)}
                </div>

                <div>
                  <h2>{candidate.name}</h2>

                  <p>
                    Candidate #{candidate.id}
                  </p>
                </div>
              </div>

              <div className="candidate-contact">
                <p>
                  {candidate.email || "Email not available"}
                </p>

                <p>
                  {candidate.phone || "Phone not available"}
                </p>
              </div>

              <div>
                <h3>Skills</h3>

                <div className="skill-list">
                  {skills.slice(0, 6).map((skill, index) => (
                    <span key={index}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <button
                className="candidate-button"
                onClick={() =>
                  setSelectedCandidate(candidate)
                }
              >
                View Candidate
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Candidates