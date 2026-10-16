# IncidentOps

IncidentOps is a cloud incident and service reliability management platform being built as a university DevOps capstone. The project will provide an operational dashboard for services and production incidents while demonstrating a complete, observable delivery path from local development to Kubernetes on AWS EKS.

## Current status

This repository currently contains the application foundation:

- A FastAPI service with metadata, liveness, database-aware readiness, Swagger, and Prometheus metrics endpoints.
- SQLAlchemy Service and Incident domain models with controlled lifecycle values and bidirectional relationships.
- A reviewed Alembic migration that creates the PostgreSQL domain schema; it has not yet been applied to a live PostgreSQL instance.
- Validated Pydantic create, update, and response schemas ready for the future CRUD API.
- A responsive React/Vite IncidentOps dashboard shell with clearly marked placeholder data.

Incident and service CRUD, live PostgreSQL migration verification, automated test coverage, Docker integration, CI/CD, Kubernetes, monitoring servers, and AWS infrastructure are planned but are **not yet implemented**.

## Stack

- **Frontend:** React, Vite, responsive CSS
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Observability foundation:** Prometheus-compatible `/metrics`

## Backend development

Python 3.12 is the target runtime. From the repository root on Windows PowerShell:

```powershell
python -m venv backend/.venv
backend\.venv\Scripts\python -m pip install -r backend\requirements.txt
Set-Location backend
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

Open:

- API metadata: `http://localhost:8000/`
- Liveness: `http://localhost:8000/health`
- Database readiness: `http://localhost:8000/ready`
- Swagger: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`

Copy `backend/.env.example` to an untracked `backend/.env` only when local PostgreSQL is available. `/ready` correctly returns HTTP 503 while the configured database is unavailable.

## Frontend development

```powershell
Set-Location frontend
npm install
npm run dev
```

The Vite development server runs at `http://localhost:3000`. Run `npm run lint` and `npm run build` before committing frontend changes.

## Planned local integration

PostgreSQL and full-stack startup will be added with Docker Compose in a later milestone. Until then, frontend placeholder metrics are intentional and the backend must be started separately.
