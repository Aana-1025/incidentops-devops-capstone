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
- [ ] User approves the plan before implementation begins.

## M1 — Repository scaffold and Git

- [x] Initialize Git on user approval.
- [ ] Create original root README outline and directory scaffold.
- [x] Add `.gitignore` entries for `.env`, `__pycache__`, `node_modules`, `.venv`, Terraform state/plan files, kubeconfig, coverage, and IDE files.
- [x] Add safe `.env.example` files with placeholders only.
- [ ] Confirm TaskBoard names/content were not copied.
- [ ] Make focused commits with meaningful messages.
- [ ] Reach at least ten meaningful commits before submission.
- [ ] Create/connect approved GitHub repository only when authorized.
- [ ] Ensure repository is public or instructor access is granted.

## M2 — Backend and database

- [ ] Configure FastAPI, settings, CORS, SQLAlchemy, and PostgreSQL session.
- [x] Define `Service` and `Incident` models with constraints and relationship.
- [x] Define validated create/update/output schemas.
- [x] Create Alembic configuration and initial migration.
- [x] Implement `/`, `/health`, database-aware `/ready`, and `/metrics`.
- [x] Implement service list/create endpoints.
- [x] Implement incident list/detail/create/update/delete endpoints.
- [x] Implement dashboard statistics endpoint.
- [x] Set/clear `resolved_at` correctly during status changes.
- [ ] Add structured errors and logging.
- [x] Verify Swagger CRUD and PostgreSQL rows.

## M3 — Frontend

- [x] Scaffold React/Vite without TaskBoard code or branding.
- [x] Build IncidentOps navigation/header and responsive layout.
- [ ] Build operational KPI/SLA-risk cards.
- [ ] Build incident filters, list/table, and severity/status badges.
- [ ] Build create/edit incident form with validation.
- [ ] Add acknowledge/investigate/resolve actions.
- [ ] Build service list/create interface.
- [ ] Add loading, empty, error, retry, and success states.
- [ ] Confirm same-origin `/api` integration.
- [ ] Verify mobile, tablet, and desktop layouts.

## M4 — Tests and quality

- [ ] Configure `pytest.ini` and `conftest.py`.
- [ ] Guarantee tests cannot use production database configuration.
- [ ] Test health and readiness behavior.
- [ ] Test incident create/list/detail/update/delete.
- [ ] Test invalid severity/status and missing required fields.
- [ ] Test 404 responses.
- [ ] Test stats and resolved timestamp behavior.
- [ ] Reach at least ten meaningful tests across at least three endpoints.
- [ ] Add frontend lint and production-build checks.
- [ ] Capture passing `pytest -v` evidence.

## M5 — Docker and Compose

- [ ] Create non-root backend Dockerfile.
- [ ] Create multi-stage, non-root frontend Dockerfile.
- [ ] Create secure Nginx same-origin proxy configuration.
- [ ] Add frontend/backend `.dockerignore` files.
- [ ] Define frontend, backend, and PostgreSQL in Compose.
- [x] Add health checks and durable local database volume.
- [ ] Run `docker compose config` and both image builds.
- [ ] Prove runtime UIDs are non-root.
- [ ] Prove `docker compose up --build` makes all services healthy.
- [ ] Capture terminal and browser evidence.

## M6 — CI/CD, GHCR, and Trivy

- [ ] Add workflow triggered on pushes and pull requests to `main`.
- [ ] Run backend tests before image build.
- [ ] Run frontend lint/build before image build.
- [ ] Build frontend and backend images.
- [ ] Scan both images with Trivy.
- [ ] Fail on HIGH/CRITICAL findings.
- [ ] Publish both images to GHCR only after gates pass.
- [ ] Tag images with Git commit SHA; do not deploy `latest`.
- [ ] Use least-privilege GitHub Actions permissions.
- [ ] Verify a deliberate test failure blocks downstream jobs.
- [ ] Capture green run URL, screenshots, packages, and scan explanation.

## M7 — Terraform and AWS preparation

- [ ] Pin Terraform and AWS provider versions.
- [ ] Define region, cluster, node, and tag variables.
- [ ] Define VPC and at least two public subnets.
- [ ] Define EKS control plane and one managed worker group.
- [ ] Add useful outputs and `terraform.tfvars.example`.
- [ ] Ignore state, plans, variable values, and credentials.
- [ ] Add cost and cleanup runbook.
- [ ] Run format, init, validate, and plan only when safe credentials are externally configured.
- [ ] Verify plan is non-empty and error-free.
- [ ] Capture plan evidence.
- [!] Obtain explicit user approval before any `terraform apply`.

## M8 — Kubernetes and Helm

- [ ] Create `k8s/namespace.yaml` for `incidentops`.
- [ ] Create Helm `Chart.yaml`, values files, helpers, and templates.
- [ ] Add backend Deployment with at least two replicas, probes, resources, and secure context.
- [ ] Add frontend Deployment with at least two replicas, probes, resources, and secure context.
- [ ] Add matching backend/frontend ClusterIP Services.
- [ ] Add PostgreSQL workload, Service, Secret references, and PVC.
- [ ] Route `/` and `/api` through Ingress using the correct Service ports.
- [ ] Add backend HPA and document Metrics Server dependency.
- [ ] Add ServiceMonitor with matching labels and named port.
- [ ] Pass `helm lint`, `helm template`, and dry-run checks.
- [ ] Deploy and verify locally before AWS.

## M9 — Observability, HPA, and troubleshooting

- [ ] Install/configure Prometheus and Grafana locally.
- [ ] Confirm backend `/metrics` format.
- [ ] Confirm Prometheus target is UP.
- [ ] Provision Grafana request-rate, latency, and error panels.
- [ ] Generate safe controlled traffic and populate panels.
- [ ] Verify HPA metrics and observe a scale event.
- [ ] Add isolated broken-image exercise and runbook.
- [ ] Add isolated broken-Service exercise and runbook.
- [ ] Demonstrate diagnosis and recovery for both faults.
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
- [ ] Write the 2–3 sentence Trivy result explanation.
- [ ] Assemble an evidence index with dates and commit SHA.
- [ ] Secret-scan source and Git history.
- [ ] Audit every rubric row against implementation and evidence.
- [ ] Rehearse the final demo from a clean checkout.
- [ ] Record a backup walkthrough if allowed.
- [ ] Submit repository URL, successful Actions URL, required screenshots, and presentation/recording.
- [ ] Submit before the deadline to avoid the 5-points-per-24-hours penalty.
