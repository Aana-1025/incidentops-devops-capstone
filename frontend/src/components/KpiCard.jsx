import PropTypes from 'prop-types'

function KpiCard({ label, value, tone }) {
  return (
    <article className={`kpi-card tone-${tone}`}>
      <div className="kpi-icon" aria-hidden="true" />
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
        <span>Placeholder data</span>
      </div>
    </article>
  )
}

KpiCard.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  tone: PropTypes.oneOf(['blue', 'red', 'violet', 'green']).isRequired,
}

export default KpiCard
