# IncidentOps Project Plan

## Delivery strategy

IncidentOps will be built and proven locally first with free/open-source tools. AWS is used only for the rubric's real VPC/EKS evidence. No application code or cloud resources are created in the planning milestone.

Quality rule for every milestone: implementation, automated verification, documentation, and evidence preparation finish together. A milestone is not complete merely because files exist.

## Milestone 0 — Rubric baseline and project controls

**Objective:** Convert the teacher's requirements into an auditable execution system before coding.

**Files:** `GRADING_REQUIREMENTS.md`, `PROJECT_PLAN.md`, `ARCHITECTURE.md`, `TODO.md`, `EVIDENCE_CHECKLIST.md`, `DECISIONS.md`.

**Verification:** Review all six documents against the teacher's full README, GRADING rubric, directory structure, and important reference configurations.

**Expected result:** Every one of the 100 points maps to planned implementation and evidence; TaskBoard-specific design is excluded.

**Evidence later required:** None for grading, but the files support the final README, demonstration, and submission audit.

**Dependencies:** None.

## Milestone 1 — Repository and professional scaffold

**Objective:** Establish an original, secure, reviewable IncidentOps repository.

**Files/components:** `.gitignore`, `.editorconfig`, `.env.example`, `README.md` outline, `LICENSE` if desired, `frontend/`, `backend/`, `scripts/`, `.github/`, `terraform/`, `k8s/`, `helm/incidentops/`, `monitoring/`, `troubleshooting/`, `evidence/README.md`.

**Verification commands:**

```powershell
git status
git check-ignore .env backend/.venv frontend/node_modules backend/app/__pycache__
git log --oneline
```

**Expected result:** No secrets or generated dependencies are tracked; naming and documentation say IncidentOps, not TaskBoard.

**Evidence eventually required:** Public/instructor-accessible repository URL and a history screenshot with at least ten meaningful commits.

**Dependencies:** Milestone 0 and user approval of the plan.

## Milestone 2 — IncidentOps application

**Objective:** Deliver a small but polished incident-management product.

**Files/components:** FastAPI configuration, database session, models, Pydantic schemas, routers, services, Alembic configuration/migration, React/Vite dashboard, reusable UI components, responsive styling, loading/empty/error states.

**Planned feature set:**

- Services: list and create operational services.
- Incidents: list, view, create, edit, acknowledge, resolve, and delete.
- Incident fields: title, description, affected service, P1–P4 severity, Open/Acknowledged/Investigating/Resolved status, assignee, created/updated/resolved timestamps.
- Dashboard: counts by severity/status, active incidents, and simple SLA-risk indicator derived from severity and elapsed time.
- Reliability endpoints: `/health`, database-aware `/ready`, `/metrics`, and Swagger `/docs`.

**Verification commands:**

```powershell
alembic upgrade head
uvicorn app.main:app --reload --port 8000
npm install
npm run build
```

Browser/API checks: `/health`, `/ready`, `/docs`, incident CRUD, service endpoints, dashboard on narrow and wide viewports.

**Expected result:** Original responsive UI calls a validated REST API backed by PostgreSQL and an Alembic-managed schema.

**Evidence eventually required:** Browser/recording, Swagger CRUD, PostgreSQL tables/migration, health and readiness output.

**Dependencies:** Milestone 1.

## Milestone 3 — Automated testing and code quality

**Objective:** Make tests the first delivery gate and exceed the five-test/three-endpoint minimum.

**Files/components:** `backend/tests/conftest.py`, isolated test database fixtures, API/unit tests, `backend/pytest.ini`; frontend lint/build configuration; optional free Ruff checks.

**Target coverage:** health, readiness, incident create/list/get/update/delete, validation, not-found behavior, statistics, resolution timestamp, and service linkage. Target at least 10 useful backend tests.

**Verification commands:**

```powershell
pytest -v
pytest --cov=app --cov-report=term-missing
npm run lint
npm run build
```

**Expected result:** Repeatable green tests use SQLite or a dedicated ephemeral test database, never production PostgreSQL.

**Evidence eventually required:** Full `pytest -v` screenshot and CI test-job output.

**Dependencies:** Milestone 2.

## Milestone 4 — Docker and local integration

**Objective:** Run the complete stack using one command and non-root containers.

**Files/components:** backend Dockerfile, frontend multi-stage Dockerfile, hardened Nginx configuration compatible with non-root runtime, `.dockerignore` files, Compose file, health checks, named PostgreSQL volume, example environment file.

**Verification commands:**

```powershell
docker compose config
docker compose build
docker compose up -d
docker compose ps
docker compose exec backend id
docker compose exec frontend id
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/ready
curl.exe http://localhost:3000
docker compose down
```

**Expected result:** Frontend, backend, and PostgreSQL become healthy; frontend proxies `/api`; runtime users are non-root.

**Evidence eventually required:** Compose terminal and `http://localhost:3000` screenshots.

**Dependencies:** Milestones 2–3.

## Milestone 5 — GitHub Actions, GHCR, and Trivy

**Objective:** Implement a traceable quality/security pipeline using free GitHub features.

**Files/components:** `.github/workflows/ci-cd.yml`, pinned action versions, least-privilege permissions, optional Dependabot configuration.

**Pipeline order:** checkout → backend tests → frontend lint/build → build two images → scan both images → push SHA-tagged images to GHCR → deploy only when explicitly enabled and configured.

**Verification:** Validate YAML locally where practical; open a pull request; confirm an intentionally failing test blocks downstream image publication, then restore and obtain a green run.

**Expected result:** Pushes to `main` run every gate; HIGH/CRITICAL CVEs fail CI; GHCR contains both immutable SHA tags.

**Evidence eventually required:** Workflow file, green run URL, job screenshots, Trivy results, GHCR screenshots, short CVE/clean-scan explanation.

**Dependencies:** Milestones 3–4 and an approved GitHub repository/push.

## Milestone 6 — Terraform design and offline validation

**Objective:** Prepare reproducible AWS VPC/EKS infrastructure without creating it yet.

**Files/components:** pinned provider/Terraform versions, provider, variables, locals/tags, VPC, at least two public subnets, EKS, one managed worker group, outputs, `terraform.tfvars.example`, cost-aware README, cleanup/runbook.

**Verification commands (safe, no resources):**

```powershell
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform plan -out=incidentops.tfplan
terraform show incidentops.tfplan
```

**Expected result:** Valid, non-empty plan with no embedded credentials and clear resources/tags.

**Evidence eventually required:** HCL files and plan screenshot.

**Dependencies:** Milestone 1. Actual plan may require AWS authentication, but secrets remain outside Git.

## Milestone 7 — Local Kubernetes and Helm proof

**Objective:** Prove the entire chart locally before paying for AWS.

**Files/components:** namespace manifest; Helm chart metadata, values, helpers, Deployments, ClusterIP Services, PostgreSQL Secret/Service/workload/PVC, Ingress, HPA, ServiceMonitor, tests; separate local/AWS values files.

**Verification commands:**

```powershell
helm lint .\helm\incidentops
helm template incidentops .\helm\incidentops -n incidentops
kubectl apply --dry-run=client -f .\k8s\namespace.yaml
helm upgrade --install incidentops .\helm\incidentops -n incidentops --create-namespace -f .\helm\incidentops\values-local.yaml
kubectl get pods,svc,ingress,hpa -n incidentops
helm list -n incidentops
```

**Expected result:** At least two frontend and two backend replicas are Running, Services match labels/ports, probes pass, and `/` plus `/api` route correctly.

**Evidence eventually required:** Final cluster screenshots are captured on EKS; local outputs serve as rehearsal and debugging proof.

**Dependencies:** Milestones 4–5 and a free local Kubernetes environment such as Docker Desktop Kubernetes or kind.

## Milestone 8 — Observability, autoscaling, and troubleshooting

**Objective:** Demonstrate operational reliability rather than only deployment.

**Files/components:** kube-prometheus-stack values, ServiceMonitor, provisioned Grafana dashboard JSON/ConfigMap, Metrics Server notes, controlled load script, broken-image and broken-Service exercises, troubleshooting runbook.

**Verification commands:**

```powershell
curl.exe http://localhost:8000/metrics
kubectl get servicemonitor -n incidentops
kubectl get hpa -n incidentops --watch
kubectl get endpoints -n incidentops
kubectl get events -n incidentops --sort-by=.lastTimestamp
```

**Expected result:** Prometheus target is UP, Grafana has populated request/latency/error panels, HPA reacts to controlled load, and both deliberate faults can be diagnosed and recovered.

**Evidence eventually required:** Metrics, Prometheus target, Grafana, HPA before/during load, broken state, diagnostic output, and recovered state.

**Dependencies:** Milestone 7.

## Milestone 9 — Short-lived AWS EKS deployment

**Objective:** Satisfy real-AWS criteria in one rehearsed, tightly controlled session.

**Preconditions:** User explicitly approves spend and `terraform apply`; AWS budget alerts are configured; local chart and images are proven; evidence checklist is ready; region and supported Kubernetes version are revalidated.

**Execution:** Apply Terraform, configure kubectl, install required cluster add-ons, deploy SHA-tagged IncidentOps release, run smoke tests and demo, capture all evidence, then destroy.

**Verification commands:**

```powershell
terraform apply incidentops.tfplan
aws eks update-kubeconfig --region <approved-region> --name <cluster-name>
kubectl get nodes
kubectl get pods,svc,ingress,hpa -n incidentops
helm list -n incidentops
terraform destroy
terraform show
```

**Expected result:** VPC, two public subnets, EKS, worker node group, application, Ingress, HPA, and monitoring are demonstrated; destroy finishes with no managed resources remaining.

**Evidence eventually required:** AWS VPC/EKS pages, cluster outputs, application, observability, and destroy completion.

**Dependencies:** Milestones 5–8, AWS authorization, and explicit user approval. This milestone must not run automatically.

## Milestone 10 — Documentation, rehearsal, and submission audit

**Objective:** Convert working engineering into an easy-to-grade 100-point submission.

**Files/components:** complete root README, architecture diagram, setup/demo/troubleshooting/cost-cleanup instructions, evidence index, final recording or presentation script.

**Verification:** Fresh-machine-style walkthrough; link checker; secret scan; compare every rubric row to a file, live result, and evidence item; confirm repository visibility/instructor access.

**Expected result:** A grader can reproduce the local stack and find evidence for every point without guessing.

**Evidence eventually required:** README, public repository URL, green workflow URL, final screenshots, and live/recorded demonstration.

**Dependencies:** All earlier milestones.

## Proposed commit sequence

Use at least ten focused commits, for example:

1. `docs: define rubric traceability and architecture`
2. `chore: scaffold IncidentOps repository`
3. `feat(api): add service and incident models`
4. `feat(api): implement incident lifecycle endpoints`
5. `feat(ui): build responsive incident dashboard`
6. `test(api): cover incident lifecycle and validation`
7. `build: containerize full local stack`
8. `ci: add test build scan and GHCR pipeline`
9. `infra: define cost-aware VPC and EKS modules`
10. `deploy: add Kubernetes and Helm resources`
11. `observability: add metrics dashboards and HPA demo`
12. `docs: finalize evidence and presentation runbook`
