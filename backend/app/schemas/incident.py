"""Pydantic schemas for production incidents."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.models import IncidentSeverity, IncidentStatus

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


class IncidentResponse(BaseModel):
    """Public representation of an incident."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    service_id: int = Field(gt=0)
    assignee: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
