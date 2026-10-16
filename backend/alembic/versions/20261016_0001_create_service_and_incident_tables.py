"""create service and incident tables

Revision ID: 20261016_0001
Revises:
Create Date: 2026-10-16
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261016_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the initial IncidentOps domain schema."""

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), server_default=sa.text("''"), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "Operational",
                "Degraded",
                "Major Outage",
                "Maintenance",
                name="service_status",
                native_enum=False,
                create_constraint=True,
            ),
            server_default=sa.text("'Operational'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_services_name"),
    )
    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), server_default=sa.text("''"), nullable=False),
        sa.Column(
            "severity",
            sa.Enum(
                "P1 Critical",
                "P2 High",
                "P3 Medium",
                "P4 Low",
                name="incident_severity",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "Open",
                "Acknowledged",
                "Investigating",
                "Resolved",
                name="incident_status",
                native_enum=False,
                create_constraint=True,
            ),
            server_default=sa.text("'Open'"),
            nullable=False,
        ),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("assignee", sa.String(length=120), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_incidents_service_id", "incidents", ["service_id"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])
    op.create_index("ix_incidents_status", "incidents", ["status"])


def downgrade() -> None:
    """Remove the initial domain schema in dependency-safe order."""

    op.drop_index("ix_incidents_status", table_name="incidents")
    op.drop_index("ix_incidents_severity", table_name="incidents")
    op.drop_index("ix_incidents_service_id", table_name="incidents")
    op.drop_table("incidents")
    op.drop_table("services")
