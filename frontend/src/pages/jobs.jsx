import { useEffect, useState } from "react"

function Jobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("/api/jobs/")
      .then((response) => response.json())
      .then((data) => {
        setJobs(data)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <div className="page">

      <div className="page-header">
        <div>
          <p className="eyebrow">OPEN POSITIONS</p>

          <h1>Jobs</h1>

          <p className="subtitle">
            Manage your open positions and find suitable candidates.
          </p>
        </div>

        <button className="primary-button">
          + New Job
        </button>
      </div>

      {loading && (
        <p>Loading jobs...</p>
      )}

      {!loading && jobs.length === 0 && (
        <div className="empty-job-card">
          <div>
            <h3>No jobs found</h3>
            <p>Create a job requirement to start finding candidates.</p>
          </div>

          <button className="secondary-button">
            Create Job
          </button>
        </div>
      )}

      <div className="job-list">

        {jobs.map((job) => (
          <div className="job-card" key={job.id}>

            <div className="job-card-top">

              <div>
                <span className="job-status">
                  ACTIVE
                </span>

                <h2>{job.title}</h2>
                <p>Job ID: #JOB-{String(job.id).padStart(3, "0")}</p>
              </div>

              <button
                className="match-button"
                onClick={() => {
                  window.dispatchEvent(
                    new CustomEvent("openMatching", {
                      detail: {
                        jobId: job.id,
                        jobTitle: job.title,
                      },
                    })
                  )
                }}
              >
                Find Candidates →
              </button>

            </div>

            <div className="job-info">

              <div>
                <span>Experience</span>

                <strong>
                  {job.experience_years ?? "Not specified"} years
                </strong>
              </div>

              <div>
                <span>Required Skills</span>

                <strong>
                {(() => {try {
                  const skills = JSON.parse(job.required_skills || "[]")
                  return skills.slice(0, 4).join(", ") || "Not specified"
                } catch {
                  return "Not specified"
                             }
                             })()}
</strong>
              </div>

              <div>
                <span>Job ID</span>

                <strong>#{job.id}</strong>
              </div>

            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default Jobs