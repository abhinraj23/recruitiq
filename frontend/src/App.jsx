import { useEffect, useState } from "react"

import Sidebar from "./sidebar"
import Dashboard from "./pages/dashboard"
import Candidates from "./pages/candidates"
import Jobs from "./pages/jobs"
import Matching from "./pages/matching"
import Enquiry from "./pages/enquiry"
import Interview from "./pages/interview"

function App() {
  const [activePage, setActivePage] = useState("Dashboard")
  const [interviewData, setInterviewData] = useState(null)
  const [selectedJob, setSelectedJob] = useState(null)

  useEffect(() => {
  const openInterview = (event) => {
    setInterviewData(event.detail)
    setActivePage("Interview")
  }

  const openMatching = (event) => {
    setSelectedJob(event.detail)
    setActivePage("Matching")
  }

  const openEnquiry = () => {
    setActivePage("Enquiry")
  }

  window.addEventListener("openInterview", openInterview)
  window.addEventListener("openMatching", openMatching)
  window.addEventListener("openEnquiry", openEnquiry)

  return () => {
    window.removeEventListener("openInterview", openInterview)
    window.removeEventListener("openMatching", openMatching)
    window.removeEventListener("openEnquiry", openEnquiry)
  }
}, [])
  const renderPage = () => {
    switch (activePage) {
      case "Dashboard":
        return <Dashboard />

      case "Candidates":
        return <Candidates />

      case "Jobs":
        return <Jobs />

      case "Matching":
        return(<Matching jobId={selectedJob?.jobId} jobTitle={selectedJob?.jobTitle}/>)

      case "Enquiry":
        return <Enquiry />

      case "Interview":
        return ( <Interview jobId={interviewData?.jobId} candidateId={interviewData?.candidateId}/> )

      default:
        return <Dashboard />
    }
  }

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  )
}

export default App