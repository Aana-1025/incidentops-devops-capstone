"""Pydantic schemas for production incidents."""

from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    computed_field,
    model_validator,
)

from app.domain import SLAStatus, evaluate_sla
from app.models import IncidentSeverity, IncidentStatus
from app.schemas.service import ServiceSummary

IncidentTitle = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
]
IncidentDescription = Annotated[str, StringConstraints(max_length=5000)]
Assignee = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]


class IncidentCreate(BaseModel):
    """Payload for declaring an incident."""

    title: IncidentTitle
    description: IncidentDescription = ""
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN
    service_id: int = Field(gt=0)
    assignee: Assignee | None = None


class IncidentUpdate(BaseModel):
    """Fields accepted when updating an incident."""

    title: IncidentTitle | None = None
    description: IncidentDescription | None = None
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None
    service_id: int | None = Field(default=None, gt=0)
    assignee: Assignee | None = None

    @model_validator(mode="after")
    def reject_invalid_nulls(self) -> "IncidentUpdate":
        """Permit clearing assignee but reject null required database fields."""

        for field in self.model_fields_set - {"assignee"}:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class IncidentResponse(BaseModel):
    """Public representation of an incident."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    service_id: int = Field(gt=0)
    service: ServiceSummary
    assignee: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None

    @computed_field
    @property
    def sla_target_minutes(self) -> int:
        """Return the configured severity target in minutes."""

        return evaluate_sla(
            self.severity,
            self.created_at,
            self.resolved_at,
        ).target_minutes

    @computed_field
    @property
    def sla_deadline(self) -> datetime:
        """Return the derived UTC SLA deadline."""

        return evaluate_sla(
            self.severity,
            self.created_at,
            self.resolved_at,
        ).deadline

    @computed_field
    @property
    def sla_status(self) -> SLAStatus:
        """Return the current derived SLA state."""

        return evaluate_sla(
            self.severity,
            self.created_at,
            self.resolved_at,
        ).status


class IncidentStatsResponse(BaseModel):
    """Database-derived dashboard counters."""

    total_incidents: int = Field(ge=0)
    open_incidents: int = Field(ge=0)
    critical_incidents: int = Field(ge=0)
    resolved_incidents: int = Field(ge=0)
    investigating_incidents: int = Field(ge=0)
    acknowledged_incidents: int = Field(ge=0)
    resolved_today: int = Field(ge=0)
    service_count: int = Field(ge=0)
