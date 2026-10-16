"""Severity-based SLA target and status policy."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
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
SLA_AT_RISK_FRACTION: Final[float] = 0.20


class SLAStatus(str, Enum):
    """Derived state of an incident relative to its SLA deadline."""

    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    BREACHED = "BREACHED"
    MET = "MET"


@dataclass(frozen=True)
class SLAEvaluation:
    """Derived SLA values returned by the API."""

    target_minutes: int
    deadline: datetime
    status: SLAStatus


def get_sla_target(severity: IncidentSeverity) -> timedelta:
    """Return the response target for an incident severity."""

    return SLA_TARGETS[severity]


def evaluate_sla(
    severity: IncidentSeverity,
    created_at: datetime,
    resolved_at: datetime | None = None,
    now: datetime | None = None,
) -> SLAEvaluation:
    """Calculate SLA state; the final 20% of an open target is at risk."""

    target = get_sla_target(severity)
    deadline = created_at + target
    comparison_time = now or datetime.now(timezone.utc)

    if resolved_at is not None:
        sla_status = SLAStatus.MET if resolved_at <= deadline else SLAStatus.BREACHED
    elif comparison_time >= deadline:
        sla_status = SLAStatus.BREACHED
    elif deadline - comparison_time <= target * SLA_AT_RISK_FRACTION:
        sla_status = SLAStatus.AT_RISK
    else:
        sla_status = SLAStatus.ON_TRACK

    return SLAEvaluation(
        target_minutes=int(target.total_seconds() // 60),
        deadline=deadline,
        status=sla_status,
    )
