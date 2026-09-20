import { useState } from "react"
import ReactMarkdown from "react-markdown"

function Enquiry() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const askQuestion = async () => {
    if (!question.trim()) return

    setLoading(true)
    setError("")
    setAnswer("")

    try {
      const response = await fetch("/api/enquiry/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.error || "Unable to process your question."
        )
      }

      if (data.error) {
        setError(data.error)
      } else {
        setAnswer(data.answer || "No answer was returned.")
      }
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">

      <div className="page-header">
        <p className="eyebrow">RECRUITER ASSISTANT</p>

        <h1>Candidate Enquiry</h1>

        <p className="subtitle">
          Ask questions about your candidates and get answers from
          recruitment data.
        </p>
      </div>

      <div className="enquiry-container">

        <div className="enquiry-input">

          <textarea
            placeholder="Ask something about your candidates..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && event.ctrlKey) {
                askQuestion()
              }
            }}
          />

          <div className="enquiry-actions">
            <span>Ctrl + Enter to ask</span>

            <button
              className="primary-button"
              onClick={askQuestion}
              disabled={loading || !question.trim()}
            >
              {loading ? "Searching..." : "Ask RecruitIQ →"}
            </button>
          </div>

        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {answer && (
          <div className="answer-card">

            <div className="answer-header">
              <div>
                <span>RECRUITER ASSISTANT</span>
                <h2>Answer</h2>
              </div>
            </div>

            <div className="answer-content">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>

          </div>
        )}

      </div>
    </div>
  )
}

export default Enquiry