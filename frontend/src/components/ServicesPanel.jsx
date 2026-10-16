import PropTypes from 'prop-types'

function statusSlug(status) {
  return status.toLowerCase().replaceAll(' ', '-')
}

function ServicesPanel({ loading, onAdd, onDelete, onEdit, services }) {
  return (
    <section className="panel services-panel" id="services" aria-labelledby="services-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Service catalog</p>
          <h2 id="services-title">Monitored services</h2>
          <p>Keep ownership context and current customer impact visible.</p>
        </div>
        <button className="button secondary" type="button" onClick={onAdd}>+ Add Service</button>
      </div>
      {loading ? (
        <div className="state-card"><span className="spinner" />Loading services…</div>
      ) : services.length === 0 ? (
        <div className="service-empty">
          <span aria-hidden="true">◇</span>
          <div><strong>Create your first monitored service</strong><p>Services are required before an incident can be reported.</p></div>
          <button className="button secondary" type="button" onClick={onAdd}>Add service</button>
        </div>
      ) : (
        <div className="service-grid">
          {services.map((service) => (
            <article className="service-card" key={service.id}>
              <div className="service-card-top">
                <span className={`service-indicator service-${statusSlug(service.status)}`} />
                <span className={`badge service-${statusSlug(service.status)}`}>{service.status}</span>
              </div>
              <h3>{service.name}</h3>
              <p>{service.description || 'No service description provided.'}</p>
              <div className="card-actions">
                <button type="button" onClick={() => onEdit(service)}>Edit</button>
                <button className="danger-link" type="button" onClick={() => onDelete(service)}>Delete</button>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  )
}

ServicesPanel.propTypes = {
  loading: PropTypes.bool.isRequired,
  onAdd: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
}

export default ServicesPanel
