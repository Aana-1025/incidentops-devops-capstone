# IncidentOps Master TODO

Legend: `[ ]` not proven, `[x]` completed and verified, `[!]` requires explicit user approval or spend.

## M0 — Planning controls

- [x] Read the teacher's complete reference README.
- [x] Read the complete 100-point grading rubric.
- [x] Inspect reference frontend, backend, Docker, CI/CD, Terraform, Kubernetes, Helm, monitoring, and troubleshooting assets.
- [x] Create `GRADING_REQUIREMENTS.md`.
- [x] Create `PROJECT_PLAN.md`.
- [x] Create `ARCHITECTURE.md`.
- [x] Create `TODO.md`.
- [x] Create `EVIDENCE_CHECKLIST.md`.
- [x] Create `DECISIONS.md`.
- [x] User approves the plan before implementation begins.

## M1 — Repository scaffold and Git

- [x] Initialize Git on user approval.
- [x] Create original root README outline and directory scaffold.
- [x] Add `.gitignore` entries for `.env`, `__pycache__`, `node_modules`, `.venv`, Terraform state/plan files, kubeconfig, coverage, and IDE files.
- [x] Add safe `.env.example` files with placeholders only.
- [x] Confirm TaskBoard names/content were not copied.
- [x] Make focused commits with meaningful messages.
- [x] Reach at least ten meaningful commits before submission.
- [x] Create/connect approved GitHub repository only when authorized.
- [ ] Ensure repository is public or instructor access is granted.

## M2 — Backend and database

- [x] Configure FastAPI, settings, SQLAlchemy, PostgreSQL session, and same-origin API access.
- [x] Define `Service` and `Incident` models with constraints and relationship.
- [x] Define validated create/update/output schemas.
- [x] Create Alembic configuration and initial migration.
- [x] Implement `/`, `/health`, database-aware `/ready`, and `/metrics`.
- [x] Implement service list/detail/create/update/delete endpoints.
- [x] Implement incident list/detail/create/update/delete endpoints.
- [x] Implement dashboard statistics endpoint.
- [x] Set/clear `resolved_at` correctly during status changes.
- [ ] Add structured errors and logging.
- [x] Verify Swagger CRUD and PostgreSQL rows.

## M3 — Frontend

- [x] Scaffold React/Vite without TaskBoard code or branding.
- [x] Build IncidentOps navigation/header and responsive layout.
- [x] Build operational KPI/SLA-risk cards.
- [x] Build incident filters, list/table, and severity/status badges.
- [x] Build create/edit incident form with validation.
- [x] Add acknowledge/investigate/resolve actions.
- [x] Build service list/create/edit/delete interface.
- [x] Add loading, empty, error, retry, and success states.
- [x] Confirm same-origin `/api` integration.
- [x] Verify mobile, tablet, and desktop layouts.

## M4 — Tests and quality

- [x] Configure `pytest.ini` and `conftest.py`.
- [x] Guarantee tests cannot use production database configuration.
- [x] Test health and readiness behavior.
- [x] Test incident create/list/detail/update/delete.
- [x] Test invalid severity/status and missing required fields.
- [x] Test 404 responses.
- [x] Test stats and resolved timestamp behavior.
- [x] Reach at least ten meaningful tests across at least three endpoints.
- [x] Add frontend lint and production-build checks.
- [ ] Capture passing `pytest -v` evidence.

## M5 — Docker and Compose

- [x] Create non-root backend Dockerfile.
- [x] Create multi-stage, non-root frontend Dockerfile.
- [x] Create secure Nginx same-origin proxy configuration.
- [x] Add frontend/backend `.dockerignore` files.
- [x] Define frontend, backend, and PostgreSQL in Compose.
- [x] Add health checks and durable local database volume.
- [x] Run `docker compose config` and both image builds.
- [x] Prove runtime UIDs are non-root.
- [x] Prove `docker compose up --build` makes all services healthy.
- [ ] Capture terminal and browser evidence.

## M6 — CI/CD, GHCR, and Trivy

- [x] Add workflow triggered on pushes and pull requests to `main`.
- [x] Run backend tests before image build.
- [x] Run frontend lint/build before image build.
- [x] Build frontend and backend images.
- [x] Scan both images with Trivy.
- [x] Fail on HIGH/CRITICAL findings.
- [x] Publish both images to GHCR only after gates pass.
- [x] Tag images with Git commit SHA; do not deploy `latest`.
- [x] Use least-privilege GitHub Actions permissions.
- [ ] Verify a deliberate test failure blocks downstream jobs.
- [x] Verify a green GitHub Actions run and both SHA-tagged GHCR packages.
- [ ] Capture Actions, package, and Trivy screenshots.

## M7 — Terraform and AWS preparation

- [x] Pin Terraform and AWS provider versions.
- [x] Define region, cluster, node, and tag variables.
- [x] Define VPC and at least two public subnets.
- [x] Define EKS control plane and one managed worker group.
- [x] Add useful outputs and `terraform.tfvars.example`.
- [x] Ignore state, plans, variable values, and credentials.
- [x] Add cost and cleanup runbook.
- [x] Run Terraform format, offline initialization, and validation without AWS credentials.
- [ ] Run a real plan only when safe credentials and the operator's `/32` API CIDR are externally configured.
- [ ] Verify plan is non-empty and error-free.
- [ ] Capture plan evidence.
- [!] Obtain explicit user approval before any `terraform apply`.

## M8 — Kubernetes and Helm

- [x] Create `k8s/namespace.yaml` for `incidentops`.
- [x] Create Helm `Chart.yaml`, values files, helpers, and templates.
- [x] Add backend Deployment with at least two replicas, probes, resources, and secure context.
- [x] Add frontend Deployment with at least two replicas, probes, resources, and secure context.
- [x] Add matching backend/frontend ClusterIP Services.
- [x] Add PostgreSQL workload, Service, Secret references, and PVC.
- [x] Route `/` and `/api` through Ingress using the correct Service ports.
- [x] Add backend HPA and document Metrics Server dependency.
- [x] Add ServiceMonitor with matching labels and named port.
- [x] Pass `helm lint`, `helm template`, and dry-run checks.
- [x] Deploy and verify locally before AWS.

## M9 — Observability, HPA, and troubleshooting

- [x] Install/configure Prometheus and Grafana locally.
- [x] Confirm backend `/metrics` format.
- [x] Confirm Prometheus target is UP.
- [x] Provision Grafana request-rate, latency, and error panels.
- [x] Generate safe controlled traffic and populate panels.
- [x] Verify HPA metrics and observe a scale event.
- [x] Add isolated broken-image exercise and runbook.
- [x] Add isolated broken-Service exercise and runbook.
- [x] Demonstrate diagnosis and recovery for both faults.
- [ ] Prepare all observability/troubleshooting evidence.

## M10 — AWS evidence window

- [!] Confirm the user-approved budget and AWS account/region.
- [ ] Configure AWS Budget alerts before infrastructure creation.
- [ ] Recheck current AWS/EKS prices and supported Kubernetes versions.
- [ ] Prepare screenshot/command checklist before apply.
- [!] Apply Terraform only after explicit approval.
- [ ] Capture VPC, public subnet, EKS, and worker-node evidence.
- [ ] Deploy exact SHA-tagged images with Helm.
- [ ] Capture Pods, Services, Helm, Ingress, HPA, Prometheus, and Grafana evidence.
- [ ] Complete the live change → CI → deployment-update rehearsal.
- [!] Run `terraform destroy` immediately after evidence capture.
- [ ] Verify no managed resources remain and capture proof.
- [ ] Recheck Billing/Cost Explorer after AWS reporting catches up.

## M11 — Documentation and submission

- [ ] Finish root README with purpose, architecture, setup, tests, deployment, observability, troubleshooting, costs, cleanup, and evidence links.
- [x] Write the 2–3 sentence Trivy result explanation.
- [ ] Assemble an evidence index with dates and commit SHA.
- [ ] Secret-scan source and Git history.
- [ ] Audit every rubric row against implementation and evidence.
- [ ] Rehearse the final demo from a clean checkout.
- [ ] Record a backup walkthrough if allowed.
- [ ] Submit repository URL, successful Actions URL, required screenshots, and presentation/recording.
- [ ] Submit before the deadline to avoid the 5-points-per-24-hours penalty.
