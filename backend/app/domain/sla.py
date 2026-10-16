"""Minimal severity-based SLA target policy."""

from datetime import timedelta
from types import MappingProxyType
from typing import Final, Mapping

from app.models import IncidentSeverity

SLA_TARGETS: Final[Mapping[IncidentSeverity, timedelta]] = MappingProxyType(
    {
        IncidentSeverity.P1_CRITICAL: timedelta(minutes=30),
        IncidentSeverity.P2_HIGH: timedelta(hours=2),
        IncidentSeverity.P3_MEDIUM: timedelta(hours=8),
        IncidentSeverity.P4_LOW: timedelta(hours=24),
    }
)


def get_sla_target(severity: IncidentSeverity) -> timedelta:
    """Return the response target for an incident severity."""

    return SLA_TARGETS[severity]
