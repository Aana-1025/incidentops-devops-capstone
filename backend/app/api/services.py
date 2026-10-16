"""Database-backed API routes for monitored services."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Incident, Service
from app.schemas import ServiceCreate, ServiceResponse, ServiceUpdate

router = APIRouter(prefix="/api/services", tags=["Services"])
SessionDependency = Annotated[Session, Depends(get_db)]


def get_service_or_404(service_id: int, session: Session) -> Service:
    """Load one service or return a consistent not-found response."""

    service = session.get(Service, service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found.",
        )
    return service


@router.get("", response_model=list[ServiceResponse])
def list_services(session: SessionDependency) -> list[Service]:
    """List services by name and then identifier for stable results."""

    statement = select(Service).order_by(Service.name.asc(), Service.id.asc())
    return list(session.scalars(statement))


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, session: SessionDependency) -> Service:
    """Return one monitored service."""

    return get_service_or_404(service_id, session)


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(payload: ServiceCreate, session: SessionDependency) -> Service:
    """Register a monitored service."""

    service = Service(**payload.model_dump())
    session.add(service)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A service with this name already exists.",
        ) from exc

    session.refresh(service)
    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    payload: ServiceUpdate,
    session: SessionDependency,
) -> Service:
    """Update only the supplied service fields."""

    service = get_service_or_404(service_id, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A service with this name already exists.",
        ) from exc

    session.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    session: SessionDependency,
) -> Response:
    """Delete a service only when it has no incident history."""

    service = get_service_or_404(service_id, session)
    incident_count = session.scalar(
        select(func.count(Incident.id)).where(Incident.service_id == service_id)
    )
    if incident_count:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service cannot be deleted while incidents reference it.",
        )

    session.delete(service)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service cannot be deleted while incidents reference it.",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
