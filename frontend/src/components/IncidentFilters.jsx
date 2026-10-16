import PropTypes from 'prop-types'

import { INCIDENT_SEVERITIES, INCIDENT_STATUSES } from '../constants.js'

function IncidentFilters({ filters, onChange, onReset, services }) {
  function updateFilter(event) {
    onChange({ ...filters, [event.target.name]: event.target.value })
  }

  const active = Object.values(filters).some(Boolean)
  return (
    <div className="filter-bar" aria-label="Incident filters">
      <select aria-label="Filter by status" name="status" value={filters.status} onChange={updateFilter}>
        <option value="">All statuses</option>
        {INCIDENT_STATUSES.map((status) => <option key={status}>{status}</option>)}
      </select>
      <select aria-label="Filter by severity" name="severity" value={filters.severity} onChange={updateFilter}>
        <option value="">All severities</option>
        {INCIDENT_SEVERITIES.map((severity) => <option key={severity}>{severity}</option>)}
      </select>
      <select aria-label="Filter by service" name="service_id" value={filters.service_id} onChange={updateFilter}>
        <option value="">All services</option>
        {services.map((service) => <option key={service.id} value={service.id}>{service.name}</option>)}
      </select>
      <input aria-label="Filter by assignee" name="assignee" value={filters.assignee} onChange={updateFilter} placeholder="Assignee" />
      <button className="reset-button" type="button" onClick={onReset} disabled={!active}>Reset filters</button>
    </div>
  )
}

IncidentFilters.propTypes = {
  filters: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired,
  onReset: PropTypes.func.isRequired,
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
}

export default IncidentFilters
