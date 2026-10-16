# IncidentOps

IncidentOps is a cloud incident and service reliability management platform being built as a university DevOps capstone. The project will provide an operational dashboard for services and production incidents while demonstrating a complete, observable delivery path from local development to Kubernetes on AWS EKS.

## Current status

This repository currently contains the application foundation:

- A FastAPI service with metadata, liveness, database-aware readiness, Swagger, and Prometheus metrics endpoints.
- SQLAlchemy Service and Incident domain models with controlled lifecycle values and bidirectional relationships.
- A reviewed Alembic migration verified against the local PostgreSQL 17 development database, including downgrade and re-upgrade.
- Validated Pydantic create, update, and response schemas used by the live CRUD API.
- Database-backed Service and Incident CRUD, incident filters, dashboard statistics, and derived SLA status responses.
- A responsive React/Vite operations dashboard connected to the live API, with incident and service CRUD, API-backed filters, KPI statistics, lifecycle controls, and derived SLA status.

Full-stack Docker integration, CI/CD, Kubernetes, monitoring servers, and AWS infrastructure are planned but are **not yet implemented**.

## Stack

- **Frontend:** React, Vite, responsive CSS
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Observability foundation:** Prometheus-compatible `/metrics`

## Local PostgreSQL

Docker Compose runs only the development database in the current milestone. PostgreSQL listens on its normal container port `5432` and is published as `localhost:5433` to avoid conflicting with an existing host database.

```powershell
docker compose up -d postgres
docker compose ps
Set-Location backend
.venv\Scripts\python -m alembic upgrade head
```

On macOS or Linux, replace `.venv\Scripts\python` with `.venv/bin/python`. The host-run backend uses:

```text
postgresql+psycopg://incidentops:incidentops@localhost:5433/incidentops
```

When the backend is containerized later, it will use Docker networking and connect to `postgres:5432`, not `localhost:5433`.

Stop the database without deleting its persistent volume:

```powershell
docker compose stop postgres
```

> **Destructive reset:** `docker compose down --volumes` permanently deletes the local IncidentOps database volume. Do not use it during normal development.

## Backend development

Python 3.12 is the target runtime. From the repository root on Windows PowerShell:

```powershell
python -m venv backend/.venv
backend\.venv\Scripts\python -m pip install -r backend\requirements.txt
docker compose up -d postgres
Set-Location backend
.venv\Scripts\python -m alembic upgrade head
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

Open:

- API metadata: `http://localhost:8000/`
- Liveness: `http://localhost:8000/health`
- Database readiness: `http://localhost:8000/ready`
- Swagger: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`

The checked-in local default connects to the Compose database on `localhost:5433`. Copy `backend/.env.example` to an untracked `backend/.env` only when you need local overrides. `/ready` returns HTTP 200 only while it can query PostgreSQL; otherwise it returns HTTP 503.

## API endpoints

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/services` | List services in deterministic name order |
| `GET` | `/api/services/{service_id}` | Get one service |
| `POST` | `/api/services` | Create a service |
| `PUT` | `/api/services/{service_id}` | Update supplied service fields |
| `DELETE` | `/api/services/{service_id}` | Delete a service without incident history |
| `GET` | `/api/incidents` | List/filter incidents by status, severity, service, or assignee |
| `GET` | `/api/incidents/stats` | Return database-derived dashboard counts |
| `GET` | `/api/incidents/{incident_id}` | Get an incident with service and SLA information |
| `POST` | `/api/incidents` | Declare an incident for an existing service |
| `PUT` | `/api/incidents/{incident_id}` | Update lifecycle and incident details |
| `DELETE` | `/api/incidents/{incident_id}` | Delete an incident |

Incident responses derive `sla_target_minutes`, `sla_deadline`, and `sla_status` from severity and timestamps; no redundant SLA columns are stored.

## Backend tests

Start the local PostgreSQL service, then run the complete suite from `backend/`:

```powershell
docker compose up -d postgres
Set-Location backend
.venv\Scripts\python -m pytest -v
```

On macOS or Linux, use `.venv/bin/python -m pytest -v`. Tests use the dedicated `incidentops_test` PostgreSQL database, apply the real Alembic migration, and clear test rows before and after every test. The normal `incidentops` development database is never used for test data. The suite uses `httpx.AsyncClient` with in-process ASGI transport rather than a live Uvicorn server.

## Frontend development

Start PostgreSQL and the backend first. In a second PowerShell terminal, run:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open `http://localhost:3000`. Vite proxies browser requests from `/api` to the host-run FastAPI server at `http://127.0.0.1:8000`, so no browser-specific backend URL is embedded in the application.

The complete local startup order is:

1. `docker compose up -d postgres`
2. From `backend/`, run `.venv\Scripts\python -m alembic upgrade head` and then `.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000`.
3. From `frontend/`, run `npm run dev`.

Useful URLs:

- Dashboard: `http://localhost:3000`
- Backend readiness: `http://localhost:8000/ready`
- Swagger API documentation: `http://localhost:8000/docs`
- Prometheus metrics: `http://localhost:8000/metrics`

Validate frontend changes with `npm run lint` and `npm run build`.

## Planned full-stack integration

PostgreSQL is available through Docker Compose. Backend and frontend containers will be added in a later milestone; until then, both applications run directly on the host and the Vite development proxy provides same-origin `/api` access.
