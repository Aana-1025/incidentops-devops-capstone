import IncidentPlaceholder from './components/IncidentPlaceholder.jsx'
import KpiCard from './components/KpiCard.jsx'
import Sidebar from './components/Sidebar.jsx'

const placeholderMetrics = [
  { label: 'Open Incidents', value: '—', tone: 'blue' },
  { label: 'Critical Incidents', value: '—', tone: 'red' },
  { label: 'Services', value: '—', tone: 'violet' },
  { label: 'Resolved Today', value: '—', tone: 'green' },
]

function App() {
  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-content">
        <header className="page-header">
          <div>
            <p className="eyebrow">Reliability overview</p>
            <h1>Cloud Incident &amp; Service Reliability</h1>
            <p className="subtitle">
              A focused command center for understanding service health and
              coordinating incident response.
            </p>
          </div>
          <span className="foundation-badge">Foundation preview</span>
        </header>

        <section className="kpi-grid" aria-label="Placeholder reliability metrics">
          {placeholderMetrics.map((metric) => (
            <KpiCard key={metric.label} {...metric} />
          ))}
        </section>

        <IncidentPlaceholder />
      </main>
    </div>
  )
}

export default App
