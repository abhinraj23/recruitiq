import { useEffect, useState } from "react"

function Interview() {
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)

    const jobId = params.get("job")
    const candidateId = params.get("candidate")

    fetch(`/api/jobs/${jobId}/candidates/${candidateId}/interview`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to generate interview questions")
        }

        return response.json()
      })
      .then((data) => {
        setQuestions(data.interview)
      })
      .catch((error) => {
        setError(error.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <div className="page">
      <div className="page-header">
        <p className="eyebrow">INTERVIEW</p>
        <h1>Interview Questions</h1>
        <p className="subtitle">
          Questions generated based on the job and candidate profile.
        </p>
      </div>

      {loading && <p>Generating interview questions...</p>}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!loading && !error && (
       <div className="detail-card interview-content">
            <pre>{questions}</pre>
       </div>
)}
    </div>
  )
}

export default Interview