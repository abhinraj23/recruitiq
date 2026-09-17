function Dashboard() {
  return (
    <div className="page">

      <div className="page-header">
        <div>
          <p className="eyebrow">OVERVIEW</p>
          <h1>Dashboard</h1>
          <p className="subtitle">
            Welcome back. Here's your recruitment overview.
          </p>
        </div>
      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <span>Total Candidates</span>
          <strong>11</strong>
        </div>

        <div className="stat-card">
          <span>Active Jobs</span>
          <strong>1</strong>
        </div>

        <div className="stat-card">
          <span>Matches Found</span>
          <strong>—</strong>
        </div>

        <div className="stat-card">
          <span>Pending Review</span>
          <strong>—</strong>
        </div>

      </div>

      <div className="dashboard-section">

        <div className="section-header">
          <div>
            <h2>Recent Jobs</h2>
            <p>Your latest recruitment requirements.</p>
          </div>
        </div>

        <div className="job-row">
          <div>
            <strong>Python / AI Developer</strong>
            <span>Job ID #JOB-001</span>
          </div>

          <span className="status">Active</span>

          <button>Find Candidates →</button>
        </div>

      </div>

      <div className="dashboard-section">

        <div className="section-header">
          <div>
            <h2>Recent Activity</h2>
            <p>Latest recruitment activity.</p>
          </div>
        </div>

        <div className="activity-list">

          <div className="activity">
            <div className="activity-dot"></div>
            <div>
              <strong>11 candidates available</strong>
              <p>Candidate database is ready for search.</p>
            </div>
          </div>

          <div className="activity">
            <div className="activity-dot"></div>
            <div>
              <strong>Python / AI Developer job created</strong>
              <p>Requirements are ready for matching.</p>
            </div>
          </div>

        </div>

      </div>

    </div>
  )
}

export default Dashboard