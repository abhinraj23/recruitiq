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

  useEffect(() => {
  const openInterview = () => {
    setActivePage("Interview")
  }

  window.addEventListener("openInterview", openInterview)

  return () => {
    window.removeEventListener("openInterview", openInterview)
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
        return <Matching />

      case "Enquiry":
        return <Enquiry />

      case "Interview":
        return <Interview />

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