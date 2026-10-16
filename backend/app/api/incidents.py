"""Database-backed API routes for production incidents."""

from datetime import datetime, time, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.models import Incident, IncidentSeverity, IncidentStatus, Service
from app.models.service import utc_now
from app.schemas import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatsResponse,
    IncidentUpdate,
)

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])
SessionDependency = Annotated[Session, Depends(get_db)]


def get_incident_or_404(incident_id: int, session: Session) -> Incident:
    """Load one incident and its service or return a consistent 404."""

    statement = (
        select(Incident)
        .options(joinedload(Incident.service))
        .where(Incident.id == incident_id)
    )
    incident = session.scalar(statement)
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found.",
        )
    return incident


def require_service(service_id: int, session: Session) -> None:
    """Reject incident writes that reference a missing service."""

    if session.get(Service, service_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referenced service not found.",
        )


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    session: SessionDependency,
    incident_status: IncidentStatus | None = Query(default=None, alias="status"),
    severity: IncidentSeverity | None = None,
    service_id: int | None = Query(default=None, gt=0),
    assignee: str | None = Query(default=None, min_length=1, max_length=120),
) -> list[Incident]:
    """List incidents newest-first with optional validated filters."""

    statement = select(Incident).options(joinedload(Incident.service))
    if incident_status is not None:
        statement = statement.where(Incident.status == incident_status)
    if severity is not None:
        statement = statement.where(Incident.severity == severity)
    if service_id is not None:
        statement = statement.where(Incident.service_id == service_id)
    if assignee is not None:
        statement = statement.where(Incident.assignee == assignee)

    statement = statement.order_by(Incident.created_at.desc(), Incident.id.desc())
    return list(session.scalars(statement))


@router.get("/stats", response_model=IncidentStatsResponse)
def get_incident_stats(session: SessionDependency) -> IncidentStatsResponse:
    """Return database-derived counts for the operations dashboard."""

    def count_incidents(*criteria: object) -> int:
        statement = select(func.count(Incident.id))
        if criteria:
            statement = statement.where(*criteria)
        return session.scalar(statement) or 0

    today_start = datetime.combine(
        datetime.now(timezone.utc).date(),
        time.min,
        tzinfo=timezone.utc,
    )
    return IncidentStatsResponse(
        total_incidents=count_incidents(),
        open_incidents=count_incidents(Incident.status != IncidentStatus.RESOLVED),
        critical_incidents=count_incidents(
            Incident.severity == IncidentSeverity.P1_CRITICAL
        ),
        resolved_incidents=count_incidents(
            Incident.status == IncidentStatus.RESOLVED
        ),
        investigating_incidents=count_incidents(
            Incident.status == IncidentStatus.INVESTIGATING
        ),
        acknowledged_incidents=count_incidents(
            Incident.status == IncidentStatus.ACKNOWLEDGED
        ),
        resolved_today=count_incidents(Incident.resolved_at >= today_start),
        service_count=session.scalar(select(func.count(Service.id))) or 0,
    )


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, session: SessionDependency) -> Incident:
    """Return one incident with service and derived SLA information."""

    return get_incident_or_404(incident_id, session)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    payload: IncidentCreate,
    session: SessionDependency,
) -> Incident:
    """Declare an incident linked to an existing service."""

    require_service(payload.service_id, session)
    incident_data = payload.model_dump()
    if payload.status == IncidentStatus.RESOLVED:
        incident_data["resolved_at"] = utc_now()

    incident = Incident(**incident_data)
    session.add(incident)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incident could not be saved due to a data conflict.",
        ) from exc

    return get_incident_or_404(incident.id, session)


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    session: SessionDependency,
) -> Incident:
    """Update supplied fields and maintain the resolution timestamp."""

    incident = get_incident_or_404(incident_id, session)
    changes = payload.model_dump(exclude_unset=True)
    if "service_id" in changes:
        require_service(changes["service_id"], session)

    next_status = changes.get("status", incident.status)
    if next_status == IncidentStatus.RESOLVED and incident.resolved_at is None:
        incident.resolved_at = utc_now()
    elif next_status != IncidentStatus.RESOLVED and incident.resolved_at is not None:
        incident.resolved_at = None

    for field, value in changes.items():
        setattr(incident, field, value)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incident could not be saved due to a data conflict.",
        ) from exc

    return get_incident_or_404(incident.id, session)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(
    incident_id: int,
    session: SessionDependency,
) -> Response:
    """Delete one incident."""

    incident = get_incident_or_404(incident_id, session)
    session.delete(incident)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Incident could not be deleted due to a data conflict.",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
