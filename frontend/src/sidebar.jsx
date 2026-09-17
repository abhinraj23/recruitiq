function Sidebar({ activePage, setActivePage }) {
  const pages = [
    "Dashboard",
    "Candidates",
    "Jobs",
    "Matching",
    "Enquiry",
  ]

  return (
    <aside className="sidebar">
      <h2>RecruitIQ</h2>

      <nav>
        {pages.map((page) => (
          <button
            key={page}
            onClick={() => setActivePage(page)}
            className={activePage === page ? "active" : ""}
          >
            {page}
          </button>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar