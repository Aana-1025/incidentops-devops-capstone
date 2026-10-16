import PropTypes from 'prop-types'
import { useState } from 'react'

import { INCIDENT_SEVERITIES, INCIDENT_STATUSES } from '../constants.js'

function initialValues(incident) {
  return incident
    ? {
        title: incident.title,
        description: incident.description,
        service_id: String(incident.service_id),
        severity: incident.severity,
        status: incident.status,
        assignee: incident.assignee ?? '',
      }
    : {
        title: '',
        description: '',
        service_id: '',
        severity: 'P3 Medium',
        status: 'Open',
        assignee: '',
      }
}

function IncidentForm({ incident, services, onCancel, onSubmit }) {
  const [values, setValues] = useState(() => initialValues(incident))
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  function updateField(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!values.title.trim() || !values.service_id) {
      setError('Add a title and choose an affected service.')
      return
    }
    setSaving(true)
    setError('')
    try {
      await onSubmit({
        ...values,
        title: values.title.trim(),
        description: values.description.trim(),
        assignee: values.assignee.trim() || null,
        service_id: Number(values.service_id),
      })
    } catch (submitError) {
      setError(submitError.message)
      setSaving(false)
    }
  }

  return (
    <form className="form-stack" onSubmit={handleSubmit}>
      {error && <div className="inline-alert error field-wide" role="alert">{error}</div>}
      <label className="field field-wide">
        <span>Incident title</span>
        <input name="title" value={values.title} onChange={updateField} maxLength="200" required autoFocus />
      </label>
      <label className="field field-wide">
        <span>Description</span>
        <textarea name="description" value={values.description} onChange={updateField} maxLength="5000" rows="4" />
      </label>
      <label className="field">
        <span>Affected service</span>
        <select name="service_id" value={values.service_id} onChange={updateField} required>
          <option value="">Choose a service</option>
          {services.map((service) => <option key={service.id} value={service.id}>{service.name}</option>)}
        </select>
      </label>
      <label className="field">
        <span>Severity</span>
        <select name="severity" value={values.severity} onChange={updateField}>
          {INCIDENT_SEVERITIES.map((severity) => <option key={severity}>{severity}</option>)}
        </select>
      </label>
      <label className="field">
        <span>Status</span>
        <select name="status" value={values.status} onChange={updateField}>
          {INCIDENT_STATUSES.map((status) => <option key={status}>{status}</option>)}
        </select>
      </label>
      <label className="field">
        <span>Assignee</span>
        <input name="assignee" value={values.assignee} onChange={updateField} maxLength="120" placeholder="Optional responder" />
      </label>
      <div className="form-actions field-wide">
        <button className="button secondary" type="button" onClick={onCancel}>Cancel</button>
        <button className="button primary" type="submit" disabled={saving || services.length === 0}>
          {saving ? 'Saving…' : incident ? 'Save incident' : 'Report incident'}
        </button>
      </div>
    </form>
  )
}

IncidentForm.propTypes = {
  incident: PropTypes.object,
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default IncidentForm
