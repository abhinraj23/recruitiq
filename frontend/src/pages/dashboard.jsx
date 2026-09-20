import { useEffect, useState } from "react"

function Dashboard() {
  const [candidateCount, setCandidateCount] = useState(0)
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch("/api/resumes/debug").then((response) => response.json()),
      fetch("/api/jobs/").then((response) => response.json()),
    ])
      .then(([candidateData, jobData]) => {
        setCandidateCount(candidateData.count)
        setJobs(jobData)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const activeJob = jobs[0]

  return (
    <div className="page">
      <div className="page-header">
        <p className="eyebrow">OVERVIEW</p>

        <h1>RecruitIQ Dashboard</h1>

        <p className="subtitle">
          Overview of your recruitment workspace.
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span>Total Candidates</span>
          <strong>{candidateCount}</strong>
        </div>

        <div className="stat-card">
          <span>Open Jobs</span>
          <strong>{jobs.length}</strong>
        </div>

        <div className="stat-card">
          <span>Top Matches</span>
          <strong>5</strong>
        </div>

        <div className="stat-card">
          <span>System Status</span>
          <strong>Ready</strong>
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Current Position</h2>
            <p>Latest recruitment requirement</p>
          </div>

          {activeJob && (
            <span className="status">ACTIVE</span>
          )}
        </div>

        {loading && (
          <div className="job-row">
            <p>Loading jobs...</p>
          </div>
        )}

        {!loading && !activeJob && (
          <div className="job-row">
            <div>
              <h3>No jobs available</h3>
              <p>Create a job to start finding candidates.</p>
            </div>
          </div>
        )}

        {!loading && activeJob && (
          <div className="job-row">
            <div>
              <h3>{activeJob.title}</h3>

              <p>
                Job ID: #JOB-
                {String(activeJob.id).padStart(3, "0")}
              </p>
            </div>

            <div>
              <strong>{candidateCount}</strong>
              <span> candidates</span>
            </div>
          </div>
        )}
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Quick Actions</h2>
            <p>Common recruiter tasks</p>
          </div>
        </div>

        <div
          className="activity quick-action"
          onClick={() => {
            if (activeJob) {
              window.dispatchEvent(
                new CustomEvent("openMatching", {
                  detail: {
                    jobId: activeJob.id,
                    jobTitle: activeJob.title,
                  },
                })
              )
            } else {
              window.dispatchEvent(
                new CustomEvent("openMatching")
              )
            }
          }}
        >
          <div className="activity-dot"></div>

          <div>
            <strong>Find candidates →</strong>

            <p>
              Match candidates against the current job
              requirement.
            </p>
          </div>
        </div>

        <div
          className="activity quick-action"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent("openEnquiry")
            )
          }
        >
          <div className="activity-dot"></div>

          <div>
            <strong>Ask RecruitIQ →</strong>

            <p>
              Ask questions about candidates and
              recruitment data.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard