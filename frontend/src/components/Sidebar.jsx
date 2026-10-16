import PropTypes from 'prop-types'

const navItems = [
  { label: 'Overview', href: '#overview', icon: '⌂' },
  { label: 'Incidents', href: '#incidents', icon: '!' },
  { label: 'Services', href: '#services', icon: '◇' },
  { label: 'Metrics', href: '#metrics', icon: '↗' },
]

function Sidebar({ connected }) {
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
            className={index === 0 ? 'nav-link active' : 'nav-link'}
            href={item.href}
            key={item.label}
          >
            <span className="nav-icon" aria-hidden="true">{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>

      <div className="sidebar-note">
        <span className={`status-dot ${connected ? '' : 'offline'}`} aria-hidden="true" />
        <div>
          <strong>{connected ? 'Live API connected' : 'API unavailable'}</strong>
          <small>{connected ? 'PostgreSQL-backed operations data' : 'Start the backend and retry'}</small>
        </div>
      </div>
    </aside>
  )
}

Sidebar.propTypes = {
  connected: PropTypes.bool.isRequired,
}

export default Sidebar
