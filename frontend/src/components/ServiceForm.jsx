import PropTypes from 'prop-types'
import { useState } from 'react'

import { SERVICE_STATUSES } from '../constants.js'

function ServiceForm({ service, onCancel, onSubmit }) {
  const [values, setValues] = useState({
    name: service?.name ?? '',
    description: service?.description ?? '',
    status: service?.status ?? 'Operational',
  })
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  function updateField(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!values.name.trim()) {
      setError('Service name is required.')
      return
    }
    setSaving(true)
    setError('')
    try {
      await onSubmit({ ...values, name: values.name.trim(), description: values.description.trim() })
    } catch (submitError) {
      setError(submitError.message)
      setSaving(false)
    }
  }

  return (
    <form className="form-stack" onSubmit={handleSubmit}>
      {error && <div className="inline-alert error field-wide" role="alert">{error}</div>}
      <label className="field field-wide">
        <span>Service name</span>
        <input name="name" value={values.name} onChange={updateField} maxLength="120" required autoFocus />
      </label>
      <label className="field field-wide">
        <span>Description</span>
        <textarea name="description" value={values.description} onChange={updateField} maxLength="2000" rows="4" />
      </label>
      <label className="field field-wide">
        <span>Current status</span>
        <select name="status" value={values.status} onChange={updateField}>
          {SERVICE_STATUSES.map((status) => <option key={status}>{status}</option>)}
        </select>
      </label>
      <div className="form-actions field-wide">
        <button className="button secondary" type="button" onClick={onCancel}>Cancel</button>
        <button className="button primary" type="submit" disabled={saving}>
          {saving ? 'Saving…' : service ? 'Save service' : 'Add service'}
        </button>
      </div>
    </form>
  )
}

ServiceForm.propTypes = {
  service: PropTypes.object,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default ServiceForm
