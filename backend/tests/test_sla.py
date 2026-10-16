"""Deterministic unit tests for the derived SLA policy."""

from datetime import datetime, timedelta, timezone

from app.domain import SLAStatus, evaluate_sla
from app.models import IncidentSeverity


def test_sla_policy_calculates_all_statuses_deterministically() -> None:
    created_at = datetime(2026, 10, 16, 10, 0, tzinfo=timezone.utc)

    on_track = evaluate_sla(
        IncidentSeverity.P1_CRITICAL,
        created_at,
        now=created_at + timedelta(minutes=5),
    )
    at_risk = evaluate_sla(
        IncidentSeverity.P1_CRITICAL,
        created_at,
        now=created_at + timedelta(minutes=25),
    )
    breached = evaluate_sla(
        IncidentSeverity.P1_CRITICAL,
        created_at,
        now=created_at + timedelta(minutes=31),
    )
    met = evaluate_sla(
        IncidentSeverity.P1_CRITICAL,
        created_at,
        resolved_at=created_at + timedelta(minutes=20),
        now=created_at + timedelta(hours=1),
    )

    assert on_track.status == SLAStatus.ON_TRACK
    assert at_risk.status == SLAStatus.AT_RISK
    assert breached.status == SLAStatus.BREACHED
    assert met.status == SLAStatus.MET
    assert on_track.target_minutes == 30
    assert on_track.deadline == created_at + timedelta(minutes=30)
