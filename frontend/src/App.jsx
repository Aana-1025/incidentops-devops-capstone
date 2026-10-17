import { useCallback, useEffect, useState } from 'react'

import IncidentFilters from './components/IncidentFilters.jsx'
import IncidentForm from './components/IncidentForm.jsx'
import IncidentTable from './components/IncidentTable.jsx'
import KpiCard from './components/KpiCard.jsx'
import Modal from './components/Modal.jsx'
import ServiceForm from './components/ServiceForm.jsx'
import ServicesPanel from './components/ServicesPanel.jsx'
import Sidebar from './components/Sidebar.jsx'
import SlaPolicyReference from './components/SlaPolicyReference.jsx'
import { EMPTY_FILTERS } from './constants.js'
import { incidentsApi, servicesApi } from './services/api.js'

const EMPTY_STATS = {
  total_incidents: 0,
  open_incidents: 0,
  critical_incidents: 0,
  resolved_incidents: 0,
  investigating_incidents: 0,
  acknowledged_incidents: 0,
  resolved_today: 0,
  service_count: 0,
}

function App() {
  const [incidents, setIncidents] = useState([])
  const [services, setServices] = useState([])
  const [stats, setStats] = useState(EMPTY_STATS)
  const [filters, setFilters] = useState(EMPTY_FILTERS)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [connected, setConnected] = useState(true)
  const [notice, setNotice] = useState('')
  const [incidentModal, setIncidentModal] = useState(null)
  const [serviceModal, setServiceModal] = useState(null)

  const loadDashboard = useCallback(async (activeFilters = filters) => {
    setLoading(true)
    setError('')
    try {
      const [incidentRows, serviceRows, summary] = await Promise.all([
        incidentsApi.list(activeFilters),
        servicesApi.list(),
        incidentsApi.stats(),
      ])
      setIncidents(incidentRows)
      setServices(serviceRows)
      setStats(summary)
      setConnected(true)
    } catch (loadError) {
      setError(loadError.message)
      setConnected(false)
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    const timer = window.setTimeout(() => loadDashboard(filters), filters.assignee ? 250 : 0)
    return () => window.clearTimeout(timer)
  }, [filters, loadDashboard])

  function showNotice(message) {
    setNotice(message)
    window.setTimeout(() => setNotice(''), 3200)
  }

  function openReportIncident() {
    if (services.length === 0) {
      showNotice('Add a monitored service before reporting an incident.')
      setServiceModal({ mode: 'create' })
      return
    }
    setIncidentModal({ mode: 'create' })
  }

  async function saveIncident(payload) {
    if (incidentModal?.incident) {
      await incidentsApi.update(incidentModal.incident.id, payload)
      showNotice('Incident updated successfully.')
    } else {
      await incidentsApi.create(payload)
      showNotice('Incident reported successfully.')
    }
    setIncidentModal(null)
    await loadDashboard(filters)
  }

  async function deleteIncident(incident) {
    if (!window.confirm(`Delete “${incident.title}”? This action cannot be undone.`)) return
    try {
      await incidentsApi.remove(incident.id)
      showNotice('Incident deleted.')
      await loadDashboard(filters)
    } catch (deleteError) {
      setError(deleteError.message)
    }
  }

  async function saveService(payload) {
    if (serviceModal?.service) {
      await servicesApi.update(serviceModal.service.id, payload)
      showNotice('Service updated successfully.')
    } else {
      await servicesApi.create(payload)
      showNotice('Service added successfully.')
    }
    setServiceModal(null)
    await loadDashboard(filters)
  }

  async function deleteService(service) {
    if (!window.confirm(`Delete “${service.name}”? Only unused services can be removed.`)) return
    try {
      await servicesApi.remove(service.id)
      showNotice('Service deleted.')
      await loadDashboard(filters)
    } catch (deleteError) {
      setError(deleteError.status === 409
        ? 'This service still has incident history. Delete or reassign those incidents first.'
        : deleteError.message)
    }
  }

  const kpis = [
    { label: 'Total incidents', value: stats.total_incidents, detail: 'All recorded activity', tone: 'plain' },
    { label: 'Open incidents', value: stats.open_incidents, detail: `${stats.investigating_incidents} investigating`, tone: 'peach' },
    { label: 'P1 critical', value: stats.critical_incidents, detail: 'Highest-impact events', tone: 'coral' },
    { label: 'Resolved', value: stats.resolved_incidents, detail: `${stats.resolved_today} resolved today`, tone: 'rose' },
    { label: 'Services', value: stats.service_count, detail: 'In the monitored catalog', tone: 'ink' },
  ]

  return (
    <div className="app-shell" id="top">
      <Sidebar connected={connected} />
      <main className="main-content">
        <header className="page-header" id="overview">
          <div>
            <p className="eyebrow">Reliability command center</p>
            <h1>Good operations start with a clear signal.</h1>
            <p className="subtitle">Track service health, coordinate incident response, and keep SLA risk visible in one focused workspace.</p>
          </div>
          <button className="button primary report-button" type="button" onClick={openReportIncident}>+ Report Incident</button>
        </header>

        {notice && <div className="toast" role="status">✓ {notice}</div>}
        {error && (
          <div className="global-alert" role="alert">
            <div><strong>We couldn’t refresh live operations data.</strong><span>{error}</span></div>
            <button className="button secondary" type="button" onClick={() => loadDashboard(filters)}>Retry</button>
          </div>
        )}

        <section className="kpi-grid" aria-label="Live reliability metrics" id="metrics">
          {kpis.map((metric) => <KpiCard key={metric.label} {...metric} value={loading ? '—' : metric.value} />)}
        </section>

        <SlaPolicyReference />

        <section className="panel incident-panel" id="incidents" aria-labelledby="incidents-title">
          <div className="section-heading incident-heading">
            <div>
              <p className="eyebrow">Incident workspace</p>
              <h2 id="incidents-title">Incident activity</h2>
              <p>{incidents.length} shown · live from PostgreSQL</p>
            </div>
            <span className="live-pill"><i />Live data</span>
          </div>
          <IncidentFilters filters={filters} onChange={setFilters} onReset={() => setFilters(EMPTY_FILTERS)} services={services} />
          <IncidentTable incidents={incidents} loading={loading} onDelete={deleteIncident} onEdit={(incident) => setIncidentModal({ mode: 'edit', incident })} onReport={openReportIncident} />
        </section>

        <ServicesPanel loading={loading} services={services} onAdd={() => setServiceModal({ mode: 'create' })} onEdit={(service) => setServiceModal({ mode: 'edit', service })} onDelete={deleteService} />
        <footer><span>IncidentOps</span> · Cloud Incident &amp; Service Reliability Management Platform</footer>
      </main>

      {incidentModal && (
        <Modal eyebrow="Incident workflow" title={incidentModal.incident ? 'Edit incident' : 'Report an incident'} onClose={() => setIncidentModal(null)}>
          <IncidentForm incident={incidentModal.incident} services={services} onCancel={() => setIncidentModal(null)} onSubmit={saveIncident} />
        </Modal>
      )}
      {serviceModal && (
        <Modal eyebrow="Service catalog" title={serviceModal.service ? 'Edit service' : 'Add a service'} onClose={() => setServiceModal(null)}>
          <ServiceForm service={serviceModal.service} onCancel={() => setServiceModal(null)} onSubmit={saveService} />
        </Modal>
      )}
    </div>
  )
}

export default App
