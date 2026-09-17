import { useEffect, useState } from "react"

function Candidates() {
  const [candidates, setCandidates] = useState([])
  const [search, setSearch] = useState("")

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
            <div className="candidate-card" key={candidate.id}>

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

              <button className="candidate-button">
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