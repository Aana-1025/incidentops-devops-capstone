const navItems = ['Overview', 'Incidents', 'Services', 'Reliability']

function Sidebar() {
  return (
    <aside className="sidebar">
      <a className="brand" href="#top" aria-label="IncidentOps home">
        <span className="brand-mark" aria-hidden="true">IO</span>
        <span>
          <strong>IncidentOps</strong>
          <small>Operations workspace</small>
        </span>
      </a>

      <nav aria-label="Primary navigation">
        {navItems.map((item, index) => (
          <a
            className={index === 0 ? 'nav-link active' : 'nav-link disabled'}
            href={index === 0 ? '#top' : `#${item.toLowerCase()}`}
            aria-disabled={index !== 0}
            key={item}
          >
            <span className="nav-dot" aria-hidden="true" />
            {item}
          </a>
        ))}
      </nav>

      <div className="sidebar-note">
        <span className="status-dot" aria-hidden="true" />
        <div>
          <strong>Foundation online</strong>
          <small>Live incident data arrives in the next milestone.</small>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
