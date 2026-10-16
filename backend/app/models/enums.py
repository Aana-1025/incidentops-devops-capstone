"""Controlled values shared by IncidentOps models and API schemas."""

from enum import Enum


class ServiceStatus(str, Enum):
    """Operational state of a monitored service."""

    OPERATIONAL = "Operational"
    DEGRADED = "Degraded"
    MAJOR_OUTAGE = "Major Outage"
    MAINTENANCE = "Maintenance"


class IncidentSeverity(str, Enum):
    """Business impact assigned to an incident."""

    P1_CRITICAL = "P1 Critical"
    P2_HIGH = "P2 High"
    P3_MEDIUM = "P3 Medium"
    P4_LOW = "P4 Low"


class IncidentStatus(str, Enum):
    """Supported states in the incident lifecycle."""

    OPEN = "Open"
    ACKNOWLEDGED = "Acknowledged"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"


def enum_values(enum_class: type[Enum]) -> list[str]:
    """Persist human-readable enum values rather than Python member names."""

    return [str(member.value) for member in enum_class]
