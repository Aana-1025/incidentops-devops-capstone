import PropTypes from 'prop-types'

function KpiCard({ detail, label, value, tone }) {
  return (
    <article className={`kpi-card tone-${tone}`}>
      <div className="kpi-top"><p>{label}</p><span className="kpi-icon" aria-hidden="true" /></div>
      <strong>{value}</strong>
      <span>{detail}</span>
    </article>
  )
}

KpiCard.propTypes = {
  detail: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  tone: PropTypes.oneOf(['coral', 'ink', 'peach', 'plain', 'rose']).isRequired,
}

export default KpiCard
