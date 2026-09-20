import { useEffect, useState } from "react"

function Interview({ jobId, candidateId }) {
  const [interview, setInterview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    fetch(`/api/jobs/${jobId}/candidates/${candidateId}/interview`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to generate interview questions")
        }

        return response.json()
      })
      .then((data) => {
        setInterview(data.interview)
      })
      .catch((error) => {
        setError(error.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [jobId, candidateId])

  return (
    <div className="page">

      <div className="page-header">
        <p className="eyebrow">INTERVIEW</p>

        <h1>Interview Questions</h1>

        <p className="subtitle">
          Questions tailored to the candidate and job requirements.
        </p>
      </div>

      {loading && (
        <div className="detail-card">
          <p>Generating interview questions...</p>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!loading && !error && interview && (
        <>
          <InterviewSection
            title="Technical Questions"
            questions={interview.technical}
          />

          <InterviewSection
            title="Experience-Based Questions"
            questions={interview.experience}
          />

          <InterviewSection
            title="Potential Gap"
            questions={interview.potential_gaps}
          />
        </>
      )}

    </div>
  )
}


function InterviewSection({ title, questions }) {
  return (
    <div className="interview-section">

      <div className="section-header">
        <h2>{title}</h2>
        <span>{questions.length} questions</span>
      </div>

      <div className="interview-question-list">

        {questions.map((item, index) => (
          <div className="interview-question-card" key={index}>

            <div className="question-number">
              {index + 1}
            </div>

            <div className="question-content">

              <h3>{item.title}</h3>

              <p className="question-text">
                {item.question}
              </p>

              <div className="assessment">
                <strong>What to assess</strong>
                <p>{item.what_to_assess}</p>
              </div>

            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default Interview