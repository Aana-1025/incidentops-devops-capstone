import PropTypes from 'prop-types'

function slug(value) {
  return value.toLowerCase().replaceAll(' ', '-')
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

function formatSlaTarget(minutes) {
  if (minutes < 60) return `${minutes} min target`
  return `${minutes / 60} hr target`
}

function IncidentTable({ incidents, loading, onDelete, onEdit, onReport }) {
  if (loading) {
    return <div className="state-card"><span className="spinner" />Loading live incidents…</div>
  }

  if (incidents.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-orbit" aria-hidden="true">✓</div>
        <h3>No incidents reported</h3>
        <p>Your operations queue is clear. Report an incident when a service needs coordinated attention.</p>
        <button className="button primary" type="button" onClick={onReport}>+ Report Incident</button>
      </div>
    )
  }

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Incident</th>
            <th>Service</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Assignee</th>
            <th>SLA</th>
            <th aria-label="Actions" />
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident) => (
            <tr key={incident.id}>
              <td>
                <button className="title-button" type="button" onClick={() => onEdit(incident)}>{incident.title}</button>
                <small>{formatDate(incident.created_at)}</small>
              </td>
              <td>{incident.service.name}</td>
              <td><span className={`badge severity-${slug(incident.severity)}`}>{incident.severity}</span></td>
              <td><span className={`badge status-${slug(incident.status)}`}>{incident.status}</span></td>
              <td>{incident.assignee || <span className="muted">Unassigned</span>}</td>
              <td>
                <span className={`badge sla-${slug(incident.sla_status)}`}>{incident.sla_status.replace('_', ' ')}</span>
                <small title={`Deadline ${formatDate(incident.sla_deadline)}`}>{formatSlaTarget(incident.sla_target_minutes)}</small>
              </td>
              <td>
                <div className="row-actions">
                  <button type="button" onClick={() => onEdit(incident)}>Edit</button>
                  <button className="danger-link" type="button" onClick={() => onDelete(incident)}>Delete</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

IncidentTable.propTypes = {
  incidents: PropTypes.arrayOf(PropTypes.object).isRequired,
  loading: PropTypes.bool.isRequired,
  onDelete: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
  onReport: PropTypes.func.isRequired,
}

export default IncidentTable
