"""Pydantic schemas for monitored services."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

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

    @model_validator(mode="after")
    def reject_explicit_nulls(self) -> "ServiceUpdate":
        """Allow omission for partial updates but reject null database fields."""

        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class ServiceSummary(BaseModel):
    """Compact service information embedded in incident responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    name: str
    status: ServiceStatus


class ServiceResponse(BaseModel):
    """Public representation of a monitored service."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    name: str
    description: str
    status: ServiceStatus
    created_at: datetime
    updated_at: datetime
