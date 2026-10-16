"""Monitored service ORM model."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

from .enums import ServiceStatus, enum_values

if TYPE_CHECKING:
    from .incident import Incident


def utc_now() -> datetime:
    """Return an aware UTC timestamp for Python-side defaults."""

    return datetime.now(timezone.utc)


class Service(Base):
    """A production service monitored by IncidentOps."""

    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("name", name="uq_services_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        server_default="",
    )
    status: Mapped[ServiceStatus] = mapped_column(
        Enum(
            ServiceStatus,
            name="service_status",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
        default=ServiceStatus.OPERATIONAL,
        server_default=ServiceStatus.OPERATIONAL.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    incidents: Mapped[list["Incident"]] = relationship(back_populates="service")
