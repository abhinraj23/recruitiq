import { useState } from "react"

function Enquiry() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")

  const askQuestion = async () => {
    if (!question.trim()) return

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

    setAnswer(
      data.answer ||
      data.error ||
      "No answer was returned."
    )
  }

  return (
    <div className="page">

      <div className="page-header">
        <div>
          <p className="eyebrow">AI ASSISTANT</p>
          <h1>Candidate Enquiry</h1>
          <p className="subtitle">
            Ask questions about candidates using grounded recruitment data.
          </p>
        </div>
      </div>

      <div className="enquiry-container">

        <div className="enquiry-input">

          <textarea
            placeholder="Example: Which candidates have experience with data pipelines?"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button
            className="primary-button"
            onClick={askQuestion}
          >
            Ask RecruitIQ →
          </button>

        </div>

        {answer && (
          <div className="answer-card">

            <div className="answer-header">
              <span>AI RESPONSE</span>
            </div>

            <p>{answer}</p>

          </div>
        )}

      </div>

    </div>
  )
}

export default Enquiry