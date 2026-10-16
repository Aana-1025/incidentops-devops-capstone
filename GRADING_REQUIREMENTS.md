# IncidentOps Grading Requirements

Source of truth: the teacher's [`session21-python/GRADING.md`](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/GRADING.md), cross-checked against the complete reference [`README.md`](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/README.md) on 2026-10-16.

This document is a traceability checklist, not a claim that an item is complete. A box is checked only after the requirement works and its evidence has been captured.

Evaluation policy: skipping a module earns zero for that section; partial credit is awarded only within a module. Incomplete items that the grader cannot evaluate do not receive partial credit, so every implemented criterion must have accessible evidence.

## Score map

| Module | Topic | Points |
|---|---|---:|
| M1 | Application — Frontend + Backend + Database | 10 |
| M2 | Testing — Pytest + Code Quality | 10 |
| M3 | Git and GitHub | 5 |
| M4 | Docker — Dockerfile + Compose | 10 |
| M5 | CI/CD — GitHub Actions Pipeline | 15 |
| M6 | DevSecOps — Trivy Security Scan | 5 |
| M7 | Terraform — AWS Infrastructure as Code | 15 |
| M8 | Kubernetes + Helm | 15 |
| M9 | Observability — Prometheus + Grafana | 10 |
| M10 | Final Presentation + Documentation | 5 |
| **Total** | | **100** |

## M1 — Application: Frontend + Backend + Database (10 points)

- [ ] **2 points:** FastAPI backend starts and responds to `/health`.
- [ ] **3 points:** At least four REST operations are implemented: GET, POST, PUT, and DELETE.
- [ ] **2 points:** PostgreSQL has at least one table managed by an Alembic migration.
- [ ] **2 points:** React/HTML frontend renders and makes API calls.
- [ ] **1 point:** UI is responsive and usable; it is not a blank page.

Required submission:

- [ ] `backend/app/` contains models, schemas, routes, and database configuration.
- [ ] `backend/alembic/versions/` contains at least one migration.
- [ ] `backend/requirements.txt` is present.
- [ ] `frontend/` contains all frontend sources.
- [ ] `docker-compose.yml` defines a working stack.
- [ ] Screenshot or short recording shows the application running in a browser.

## M2 — Testing: Pytest + Code Quality (10 points)

- [ ] **3 points:** `pytest` runs without errors.
- [ ] **4 points:** At least five test cases cover at least three API endpoints.
- [ ] **2 points:** Tests use a test database or mocks, never the production database.
- [ ] **1 point:** `pytest.ini` or `conftest.py` exists and is correctly configured.

Required submission:

- [ ] `backend/tests/` contains all tests.
- [ ] `backend/pytest.ini` or `backend/conftest.py` is present.
- [ ] Terminal screenshot shows all tests passing with `pytest -v`.

## M3 — Git and GitHub (5 points)

- [ ] **2 points:** A public GitHub repository is linked in the submission form, or instructor access is granted as allowed by the submission requirement.
- [ ] **2 points:** Commit messages are meaningful; avoid messages such as `update`, `fix`, or `test`.
- [ ] **1 point:** `.gitignore` excludes `.env`, `__pycache__`, `node_modules`, and `.venv`.

Required submission:

- [ ] GitHub repository URL.
- [ ] Commit-history screenshot showing at least ten commits.

## M4 — Docker: Dockerfile + Compose (10 points)

- [ ] **2 points:** `backend/Dockerfile` builds successfully.
- [ ] **3 points:** `frontend/Dockerfile` uses a Node build stage and an Nginx runtime stage.
- [ ] **2 points:** Both runtime images run as non-root users.
- [ ] **3 points:** `docker compose up --build` starts frontend, backend, and PostgreSQL.

Required submission:

- [ ] `backend/Dockerfile`.
- [ ] `frontend/Dockerfile`.
- [ ] `docker-compose.yml`.
- [ ] Terminal screenshot shows `docker compose up --build` running successfully.
- [ ] Browser screenshot shows IncidentOps at `http://localhost:3000`.

## M5 — CI/CD: GitHub Actions Pipeline (15 points)

- [ ] **1 point:** `.github/workflows/` contains at least one workflow YAML file.
- [ ] **1 point:** Pipeline triggers on every push to `main`.
- [ ] **3 points:** Pytest runs as a pipeline job and a failing test fails/stops the build.
- [ ] **2 points:** The React frontend is built in the pipeline.
- [ ] **3 points:** Both frontend and backend Docker images are built.
- [ ] **3 points:** Both images are pushed to GitHub Container Registry (GHCR).
- [ ] **2 points:** Image tags use the Git commit SHA, not `latest`.

Required submission:

- [ ] All `.github/workflows/` YAML files.
- [ ] URL of a successful green GitHub Actions run.
- [ ] GHCR package-page screenshot showing both images with SHA-based tags.

## M6 — DevSecOps: Trivy Security Scan (5 points)

- [ ] **3 points:** CI scans both backend and frontend images with Trivy.
- [ ] **1 point:** CI fails on HIGH or CRITICAL vulnerabilities.
- [ ] **1 point:** Student can explain one discovered CVE, or explain what a clean result means.

Required submission:

- [ ] Trivy steps are visible in the GitHub Actions workflow.
- [ ] Pipeline screenshot shows Trivy output for both images; clean or findings are acceptable.
- [ ] A 2–3 sentence explanation says what Trivy scanned and what the result means.

## M7 — Terraform: AWS Infrastructure as Code (15 points)

- [ ] **2 points:** `terraform/` contains valid HCL files.
- [ ] **1 point:** `terraform init` completes without errors.
- [ ] **2 points:** `terraform plan` produces a non-empty, error-free plan.
- [ ] **3 points:** A VPC with at least two public subnets is provisioned.
- [ ] **4 points:** An EKS cluster with at least one worker node group is provisioned.
- [ ] **2 points:** `terraform destroy` cleanly removes all resources.
- [ ] **1 point:** `terraform.tfvars.example` is present and contains no real credentials.

Required submission:

- [ ] All `terraform/*.tf` files.
- [ ] Screenshot of `terraform plan` output.
- [ ] AWS Console screenshot shows the VPC and EKS cluster in the expected region.
- [ ] Screenshot shows successful `terraform destroy` completion, proving cost cleanup.

Critical warning: never commit AWS access keys, secret keys, kubeconfig content, passwords, or other credentials. The grading team rejects submissions if secrets appear anywhere in Git history.

## M8 — Kubernetes + Helm (15 points)

- [ ] **1 point:** `k8s/namespace.yaml` exists and applies cleanly.
- [ ] **3 points:** A chart under `helm/` contains `Chart.yaml`, `values.yaml`, and templates.
- [ ] **3 points:** `helm upgrade --install` deploys without errors.
- [ ] **2 points:** Backend and frontend Deployments run at least two replicas each.
- [ ] **2 points:** ClusterIP Services expose backend and frontend.
- [ ] **2 points:** Ingress routes `/` to frontend and `/api` to backend.
- [ ] **2 points:** `kubectl get pods -n incidentops` shows every Pod in `Running` state.

Required submission:

- [ ] `k8s/` contains namespace and bootstrap manifests.
- [ ] `helm/` contains the complete chart.
- [ ] Screenshot: all Pods are Running.
- [ ] Screenshot: `kubectl get svc -n incidentops`.
- [ ] Screenshot: `helm list -n incidentops`.
- [ ] Browser screenshot: application opened through the Ingress hostname or LoadBalancer address.

## M9 — Observability: Prometheus + Grafana (10 points)

- [ ] **2 points:** Backend `/metrics` returns Prometheus-formatted output.
- [ ] **3 points:** Prometheus is installed in the cluster and scrapes IncidentOps.
- [ ] **2 points:** Grafana is installed and accessible.
- [ ] **3 points:** At least one Grafana panel displays live requests, latency, or error-rate data.

Required submission:

- [ ] `monitoring/` contains Prometheus and Grafana Helm values.
- [ ] Screenshot shows `curl http://<backend>/metrics` output.
- [ ] Prometheus Targets screenshot shows IncidentOps as `UP`.
- [ ] Grafana screenshot shows at least one populated application panel.

## M10 — Final Presentation + Documentation (5 points)

- [ ] **2 points:** Root `README.md` explains what IncidentOps does.
- [ ] **3 points:** Live demo commits a change, watches CI run, and shows the deployment update.

Required submission:

- [ ] Root `README.md`.
- [ ] Live presentation, or a recorded walkthrough if the session is remote.

## Exact final submission checklist

### Application

- [ ] GitHub repository URL submitted.
- [ ] Application runs with `docker compose up --build`.
- [ ] At least four REST API operations are implemented.
- [ ] Alembic migration exists.

### Testing

- [ ] Pytest passes and a screenshot is submitted.
- [ ] At least five tests exist.

### Docker

- [ ] Backend Dockerfile builds.
- [ ] Frontend Dockerfile is multi-stage.
- [ ] Both Dockerfiles use a non-root runtime user.

### CI/CD and security

- [ ] GitHub Actions workflow exists and runs on pushes to `main`.
- [ ] Pytest runs in CI.
- [ ] Images are pushed to GHCR with SHA tags.
- [ ] Trivy scans both images and fails on HIGH/CRITICAL findings.
- [ ] No secrets are committed.

### Terraform and AWS

- [ ] Terraform plan output is submitted.
- [ ] VPC and EKS are provisioned and shown in AWS Console.
- [ ] Terraform destroy output is submitted.

### Kubernetes, Helm, and observability

- [ ] All Pods Running screenshot is submitted.
- [ ] Helm release screenshot is submitted.
- [ ] Application is accessible through Ingress.
- [ ] `/metrics`, Prometheus `UP`, and populated Grafana screenshots are submitted.

### Documentation and presentation

- [ ] README is present.
- [ ] Presentation or recording is completed.

## Required by the reference README even where the marks table is not explicit

These are part of the teacher's stated minimum DevOps architecture and final demonstration, so they remain in scope:

- [ ] Health and readiness endpoints are distinct; readiness verifies database access.
- [ ] HPA exists, has CPU requests and a metrics provider, and is demonstrated under controlled load.
- [ ] A Git commit and CI quality-gate flow are demonstrated.
- [ ] Docker images and GHCR packages are demonstrated.
- [ ] Terraform infrastructure code is explained.
- [ ] Kubernetes Pods and Services are shown.
- [ ] Helm concepts and release are explained.
- [ ] Ingress, autoscaling, Prometheus, and Grafana are demonstrated.
- [ ] Broken-image and broken-Service exercises are diagnosed using Pod status, descriptions, events, labels, and endpoints.

## Grading policy and non-negotiable warnings

- [ ] Submission is on time; the policy deducts **5 points per 24 hours late**.
- [ ] IncidentOps is visibly original in domain, data model, copy, UI, API, and branding.
- [ ] The project is not a direct TaskBoard clone. A direct clone or plagiarized submission receives **zero for all modules**.
- [ ] DevOps architecture may follow the teacher's reference architecture.
- [ ] AWS resources are destroyed immediately after evidence capture; students are responsible for runaway costs.
