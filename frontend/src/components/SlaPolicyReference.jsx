const SLA_POLICIES = [
  { severity: 'P1 Critical', target: '30 min', tone: 'critical' },
  { severity: 'P2 High', target: '2 h', tone: 'high' },
  { severity: 'P3 Medium', target: '8 h', tone: 'medium' },
  { severity: 'P4 Low', target: '24 h', tone: 'low' },
]

function SlaPolicyReference() {
  return (
    <section className="sla-policy" aria-labelledby="sla-policy-title">
      <div className="sla-policy-copy">
        <p className="eyebrow">Response targets</p>
        <h2 id="sla-policy-title">SLA policy</h2>
        <p>Resolution targets used to calculate incident risk.</p>
      </div>
      <div className="sla-policy-list">
        {SLA_POLICIES.map((policy) => (
          <div className={`sla-policy-item sla-policy-${policy.tone}`} key={policy.severity}>
            <span>{policy.severity}</span>
            <strong>{policy.target}</strong>
          </div>
        ))}
      </div>
    </section>
  )
}

export default SlaPolicyReference
