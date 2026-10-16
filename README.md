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
- A three-service Docker Compose stack with unprivileged backend and frontend runtimes, automated migrations, health checks, and an Nginx same-origin API proxy.
- A locally verified Kubernetes/Helm release with NGINX Ingress, CPU autoscaling, Prometheus scraping, and a provisioned Grafana dashboard.

CI/CD, local Kubernetes, and application observability are implemented. Terraform/AWS and the isolated troubleshooting exercises remain planned.

## Stack

- **Frontend:** React, Vite, responsive CSS
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Observability foundation:** Prometheus-compatible `/metrics`

## Run with Docker Compose

Build and start the complete application from the repository root:

```powershell
docker compose up --build
```

The stack applies Alembic migrations before starting the API. Open:

- Dashboard: `http://localhost:3000`
- Swagger: `http://localhost:8000/docs`
- Liveness: `http://localhost:8000/health`
- Database readiness: `http://localhost:8000/ready`
- Metrics: `http://localhost:8000/metrics`

Inside Docker, the backend reaches PostgreSQL at `postgres:5432`; the browser sends relative `/api` requests to Nginx, which proxies them to `backend:8000`.

Stop the stack while preserving the named PostgreSQL volume:

```powershell
docker compose down
```

> **Destructive reset:** `docker compose down -v` removes the IncidentOps PostgreSQL volume and all local application data. Do not use it during normal development.

## Local PostgreSQL and host development

For host-run backend development, PostgreSQL listens on its normal container port `5432` and is published as `localhost:5433` to avoid conflicting with an existing host database.

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

The Compose backend instead uses Docker networking and connects to `postgres:5432`, not `localhost:5433`.

Stop the database without deleting its persistent volume:

```powershell
docker compose stop postgres
```

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

## CI/CD and container security

Every push to `main` and every pull request targeting `main` runs the `IncidentOps CI/CD` GitHub Actions workflow. The quality job provisions an ephemeral PostgreSQL 17 service, runs all backend tests against the isolated `incidentops_test` database, then runs frontend lint and the production build.

After quality checks pass, the pipeline builds both runtime images and scans their operating-system and application packages with Trivy. Any known `HIGH` or `CRITICAL` vulnerability fails the job. Only successful scans permit a `main` push to publish these immutable images through the built-in `GITHUB_TOKEN`:

```text
ghcr.io/aana-1025/incidentops-backend:<full-git-sha>
ghcr.io/aana-1025/incidentops-frontend:<full-git-sha>
```

The workflow does not publish a `latest` tag and does not deploy to Kubernetes. Package visibility is managed in GitHub Container Registry.

Trivy inspects the operating-system and language-package contents of both runtime images for known `HIGH` and `CRITICAL` CVEs. The initial preflight found unfixed Debian base-image findings plus three fixable Alpine packages in the frontend; moving the backend to the current official Python Alpine image and upgrading the frontend runtime packages produced clean blocking scans without suppressing findings.

## Kubernetes and Helm

The chart in `helm/incidentops/` deploys two frontend replicas, two backend replicas, one PostgreSQL StatefulSet, and a persistent 1 GiB database volume in the `incidentops` namespace. ClusterIP Services keep workloads internal, while a configurable Ingress sends `/` to the frontend and `/api` to the backend. The chart defaults to the verified immutable GHCR tag recorded in `values.yaml`; it never relies on `latest`.

Each application workload has lightweight CPU/memory requests and limits. Backend liveness uses `/health`, backend readiness uses the database-aware `/ready`, and frontend probes request `/`. A revision-scoped migration Job waits for PostgreSQL and runs `alembic upgrade head` once per Helm release; backend init containers wait for the database to reach the Alembic head before Uvicorn starts, avoiding migrations racing across replicas.

Prerequisites are a working Kubernetes context, `kubectl`, Helm, and an Ingress controller. For Docker Desktop Kubernetes, install the free NGINX controller without binding a host LoadBalancer port:

```powershell
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx `
  --namespace ingress-nginx --create-namespace `
  --set controller.service.type=NodePort --wait
```

Validate and install IncidentOps:

```powershell
kubectl apply --dry-run=client -f .\k8s\namespace.yaml
helm lint .\helm\incidentops -f .\helm\incidentops\values-local.yaml
helm template incidentops .\helm\incidentops -n incidentops `
  -f .\helm\incidentops\values-local.yaml
kubectl apply -f .\k8s\namespace.yaml
helm upgrade --install incidentops .\helm\incidentops `
  --namespace incidentops --create-namespace `
  -f .\helm\incidentops\values-local.yaml `
  --wait --wait-for-jobs --timeout 5m
```

The local chart configuration uses the hostless `nginx` Ingress class and a clearly development-only database password. Supply a secure value outside Git for any non-local environment. To exercise the Ingress locally without editing the hosts file:

```powershell
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8088:80
```

Open `http://127.0.0.1:8088`; API calls remain same-origin under `/api`. Verify the release with:

```powershell
kubectl get pods,deployments,svc,ingress,pvc -n incidentops
helm list -n incidentops
kubectl port-forward -n incidentops service/incidentops-backend 18000:8000
```

The direct backend forward exposes `/health` and `/ready` at `http://127.0.0.1:18000`. A normal PostgreSQL pod restart preserves data on the PVC. When the local data is no longer needed, uninstall with `helm uninstall incidentops -n incidentops`; this removes the release-owned PVC and its data.

## Autoscaling and observability

The backend HPA maintains 2–5 replicas and targets 50% average CPU utilization. It depends on Metrics Server; Docker Desktop requires the local-only kubelet TLS compatibility flag shown below. The PostgreSQL container and Service continue to use port `5432` inside Kubernetes.

```powershell
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install metrics-server metrics-server/metrics-server `
  --namespace kube-system --version 3.14.0 `
  --set 'args[0]=--kubelet-insecure-tls' --wait --timeout 5m
kubectl top nodes
kubectl get hpa incidentops-backend -n incidentops --watch
```

`monitoring/kube-prometheus-stack-values.yaml` installs a lightweight, local-only Prometheus and Grafana stack. Prometheus explicitly selects the IncidentOps namespace and the chart-managed ServiceMonitor; Grafana provisions the `IncidentOps Observability` dashboard from source with request-rate, p95-latency, and 5xx-rate panels. No Grafana credential is committed.

```powershell
helm upgrade --install kube-prometheus-stack `
  prometheus-community/kube-prometheus-stack `
  --namespace monitoring --create-namespace --version 92.10.0 `
  -f .\monitoring\kube-prometheus-stack-values.yaml `
  --wait --timeout 10m
kubectl get pods -n monitoring
kubectl get servicemonitor -n incidentops
kubectl port-forward -n monitoring service/kube-prometheus-stack-prometheus 9090:9090
kubectl port-forward -n monitoring service/kube-prometheus-stack-grafana 3001:80
```

Open Prometheus at `http://127.0.0.1:9090/targets` and confirm `incidentops-backend` is `UP`. Useful queries are `sum(rate(http_requests_total[1m]))`, p95 over `http_request_duration_seconds_bucket`, and the `5..` status rate. Open Grafana at `http://127.0.0.1:3001`; retrieve its generated local admin password directly from the Kubernetes Secret only when needed, and never copy it into files or evidence.

For a controlled HPA demonstration, create a temporary namespaced load Deployment, watch CPU and replicas, and delete that exact Deployment immediately afterward. Keep the load modest for the available local CPU and confirm the application stays ready:

```powershell
kubectl create deployment incidentops-load -n incidentops `
  --image=curlimages/curl:8.23.0 -- /bin/sh -c `
  "while true; do curl -s -o /dev/null http://incidentops-backend:8000/health; done"
kubectl scale deployment incidentops-load -n incidentops --replicas=4
kubectl get hpa incidentops-backend -n incidentops --watch
kubectl delete deployment incidentops-load -n incidentops
```
