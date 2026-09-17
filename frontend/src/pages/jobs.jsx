function Jobs() {
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


      <div className="job-list">

        <div className="job-card">

          <div className="job-card-top">

            <div>
              <span className="job-status">
                ACTIVE
              </span>

              <h2>Python / AI Developer</h2>

              <p>
                Job ID: #JOB-001
              </p>
            </div>

            <button className="match-button">
              Find Candidates →
            </button>

          </div>


          <div className="job-info">

            <div>
              <span>Required Skills</span>

              <div className="job-skills">
                <span>Python</span>
                <span>FastAPI</span>
                <span>AI</span>
                <span>SQL</span>
              </div>
            </div>


            <div>
              <span>Experience</span>
              <strong>0–3 years</strong>
            </div>


            <div>
              <span>Applicants</span>
              <strong>11 candidates</strong>
            </div>

          </div>

        </div>


        <div className="empty-job-card">

          <div>
            <h3>Need to hire for another position?</h3>

            <p>
              Create a new job requirement to start finding candidates.
            </p>
          </div>

          <button className="secondary-button">
            Create Job
          </button>

        </div>

      </div>

    </div>
  )
}

export default Jobs