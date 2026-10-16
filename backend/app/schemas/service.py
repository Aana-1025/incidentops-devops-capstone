"""Pydantic schemas for monitored services."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.models import ServiceStatus

ServiceName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=120),
]
ServiceDescription = Annotated[str, StringConstraints(max_length=2000)]


class ServiceCreate(BaseModel):
    """Payload for registering a monitored service."""

    name: ServiceName
    description: ServiceDescription = ""
    status: ServiceStatus = ServiceStatus.OPERATIONAL


class ServiceUpdate(BaseModel):
    """Fields accepted when updating a service."""

    name: ServiceName | None = None
    description: ServiceDescription | None = None
    status: ServiceStatus | None = None


class ServiceResponse(BaseModel):
    """Public representation of a monitored service."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    name: str
    description: str
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime
