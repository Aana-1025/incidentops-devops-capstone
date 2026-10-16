function IncidentPlaceholder() {
  return (
    <section className="incident-panel" aria-labelledby="incident-heading">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Incident workspace</p>
          <h2 id="incident-heading">Active incidents</h2>
        </div>
        <span className="demo-label">Demo placeholder</span>
      </div>

      <div className="empty-state">
        <div className="empty-icon" aria-hidden="true">◎</div>
        <h3>Incident data is not connected yet</h3>
        <p>
          The application shell is ready. Incident workflows and live API data
          will be implemented in the next approved application milestone.
        </p>
      </div>
    </section>
  )
}

export default IncidentPlaceholder
