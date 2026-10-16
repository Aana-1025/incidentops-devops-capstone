# IncidentOps Evidence Checklist

## Evidence rules

- Capture evidence only after the relevant check passes.
- Keep the application name, repository, AWS region, namespace, date, and deployed commit SHA visible where practical.
- Use readable full-window captures; do not crop away command names, statuses, resource names, or timestamps.
- Never show passwords, tokens, access keys, kubeconfig, `.env`, GitHub secrets, or Terraform state.
- Save originals under an untracked or deliberately reviewed `evidence/` folder using the suggested names below.
- Record the successful Git commit SHA in `evidence/README.md` so CI, GHCR, Helm values, and the application can be traced to one revision.

## Application and database — M1

- [ ] `m1-01-dashboard-desktop.png`: IncidentOps dashboard with real service/incident data.
- [ ] `m1-02-dashboard-mobile.png`: responsive narrow viewport.
- [ ] `m1-03-create-incident.png`: validated incident form or short CRUD recording.
- [ ] `m1-04-incident-lifecycle.png`: incident shown as Acknowledged/Investigating/Resolved with timestamps.
- [ ] `m1-05-swagger.png`: FastAPI `/docs` showing IncidentOps endpoints.
- [ ] `m1-06-health-ready.txt/png`: `/health` UP and `/ready` READY.
- [ ] `m1-07-database.png`: PostgreSQL `services` and `incidents` tables/rows; no credentials visible.
- [ ] `m1-08-alembic.png`: `alembic current` and migration upgrade output.
- [ ] Short browser recording proves create, read, update, and delete through the UI/API.

Reproduce the local UI evidence with PostgreSQL on `localhost:5433`, FastAPI on `localhost:8000`, and Vite on `localhost:3000`. Use temporary records, demonstrate API-backed filters and the Open → Investigating → Resolved transition, then remove the records so the empty state is visible again.

## Testing — M2

- [ ] `m2-01-pytest.png`: complete `cd backend` / `pytest -v` command and the final passing summary in one readable terminal capture.
- [ ] Output visibly proves all 16 tests pass with zero failures; the rubric minimum is five.
- [ ] Tests shown cover at least three different endpoints.
- [ ] `tests/conftest.py` and terminal/database evidence prove `incidentops_test` isolation from the normal `incidentops` database.
- [ ] Optional `m2-02-coverage.png`: useful coverage report for portfolio quality.

## Git and GitHub — M3

- [ ] Copy the final public repository URL, or prove instructor access.
- [ ] `m3-01-commit-history.png`: GitHub commit history with at least ten meaningful messages.
- [ ] `m3-02-gitignore.png`: relevant `.gitignore` entries.
- [ ] Confirm `.env`, `.venv`, `node_modules`, `__pycache__`, Terraform state, plans, and kubeconfig are absent from the repository.
- [ ] Record final commit SHA.

## Docker and Compose — M4

- [ ] `m4-01-compose-build.png`: `docker compose up --build` with all three services started.
- [ ] `m4-02-compose-ps.png`: frontend, backend, and PostgreSQL healthy/running.
- [ ] `m4-03-local-browser.png`: `http://localhost:3000` loaded.
- [ ] `m4-04-images.png`: both locally built image names/tags.
- [ ] `m4-05-nonroot.png`: runtime identity/UID proves backend and frontend are non-root.
- [ ] Source evidence includes backend Dockerfile, frontend multi-stage Dockerfile, and Compose file.

Reproduce this evidence from the repository root with `docker compose up --build -d`, `docker compose ps`, `docker compose exec backend id`, and `docker compose exec frontend id`. Then load `http://localhost:3000`; capture screenshots manually only after all three services report healthy, and do not expose environment values.

## GitHub Actions and GHCR — M5

- [ ] Save the successful GitHub Actions run URL in `evidence/README.md` with its exact commit SHA.
- [ ] `m5-01-actions-green.png`: overall green workflow with commit SHA.
- [ ] `m5-02-test-job.png`: backend test and frontend build steps passed.
- [ ] `m5-03-image-builds.png`: both image builds passed.
- [ ] `m5-04-ghcr-backend.png`: backend GHCR package with SHA tag.
- [ ] `m5-05-ghcr-frontend.png`: frontend GHCR package with SHA tag.
- [ ] `m5-06-ghcr-packages.png`: both package names and their matching full-SHA tags visible together where GitHub permits.
- [ ] Verify displayed tag is a commit SHA and not `latest`.
- [ ] Source evidence includes `.github/workflows/ci-cd.yml` and `on: push: branches: [main]`.
- [ ] Demonstration artifact: optional failed-run screenshot proving failed tests block publish/deploy.

## Trivy — M6

- [ ] `m6-01-trivy-backend.png`: backend scan output.
- [ ] `m6-02-trivy-frontend.png`: frontend scan output.
- [ ] Trivy screenshots come from the successful SHA-matched Actions run and visibly identify which image was scanned.
- [ ] Workflow source visibly contains `HIGH,CRITICAL` and failing exit code.
- [ ] Save a 2–3 sentence explanation of what was scanned and either one CVE/remediation or the meaning of a clean scan.

## Terraform and AWS — M7

Before capture: hide account IDs where not needed and never reveal credentials.

- [ ] `m7-01-fmt-validate.png`: format and validation success.
- [ ] `m7-02-terraform-plan.png`: non-empty, error-free plan summary.
- [ ] `m7-03-vpc-console.png`: expected tagged VPC in the approved region.
- [ ] `m7-04-public-subnets.png`: at least two public subnets, ideally showing distinct Availability Zones.
- [ ] `m7-05-eks-console.png`: IncidentOps EKS cluster Active in the expected region.
- [ ] `m7-06-nodegroup.png`: at least one managed worker node group Active.
- [ ] `m7-07-kubectl-nodes.png`: worker nodes Ready.
- [ ] `m7-08-terraform-destroy.png`: destroy completion with removed-resource summary.
- [ ] `m7-09-post-destroy.png`: console/CLI verification that IncidentOps cluster and cost-driving resources no longer exist.
- [ ] Source evidence includes all `.tf` files and credential-free `terraform.tfvars.example`.

## Kubernetes and Helm — M8

- [ ] `m8-01-namespace.png`: namespace exists/applies cleanly.
- [ ] `m8-02-pods.png`: every Pod Running/Ready; frontend and backend each show at least two replicas.
- [ ] `m8-03-services.png`: ClusterIP frontend/backend Services and ports.
- [ ] `m8-04-deployments.png`: desired/ready replica counts.
- [ ] `m8-05-helm-list.png`: deployed IncidentOps release and namespace.
- [ ] `m8-06-ingress.png`: Ingress host/address and `/` plus `/api` paths.
- [ ] `m8-07-ingress-browser.png`: application accessed through Ingress hostname or LoadBalancer address.
- [ ] `m8-08-api-through-ingress.png`: `/api/incidents` reached through Ingress.
- [ ] `m8-09-pvc.png`: PostgreSQL PVC is `Bound`; a pod restart preserves a temporary record.
- [ ] `m8-10-self-healing.png`: frontend and backend return to two Ready replicas after one pod from each Deployment is deleted.
- [ ] `m8-11-helm-upgrade.png`: harmless upgrade completes and `helm list` shows the new deployed revision.
- [ ] `m8-12-migration-job.png`: the release migration Job completes before both backend replicas become Ready.
- [ ] Source evidence includes `k8s/namespace.yaml` and complete `helm/incidentops/` chart.

## HPA evidence required by the reference README/final demo

- [ ] `hpa-01-before.png`: HPA at baseline with metrics available.
- [ ] `hpa-02-load.png`: controlled load generator running.
- [ ] `hpa-03-scale.png`: HPA/backend replica count increased, or a recorded explanation if the environment cannot create sufficient safe load.
- [ ] `hpa-04-after.png`: load stopped and system recovering toward baseline.
- Capture `kubectl top pods -n incidentops`, `kubectl get hpa -n incidentops`, and the backend Deployment together. The verified local rehearsal scaled from 2 to the configured maximum of 5 and returned to 2 after cleanup.

## Prometheus and Grafana — M9

- [ ] `m9-01-metrics.png`: `curl http://<backend>/metrics` with Prometheus-formatted output.
- [ ] `m9-02-prometheus-target.png`: IncidentOps target state `UP`.
- [ ] `m9-03-grafana-request-rate.png`: populated HTTP request panel.
- [ ] `m9-04-grafana-latency-errors.png`: populated latency or error-rate panel.
- [ ] `m9-05-monitoring-pods.png`: Prometheus/Grafana workloads running.
- [ ] Source evidence includes monitoring values and provisioned dashboard artifacts.
- For target evidence, show the `incidentops-backend` job as `UP` without exposing Kubernetes Secrets. For dashboard evidence, generate controlled requests first and keep the request-rate and p95 panels' live points visible.

## Troubleshooting demonstration required by the reference README

### Broken image

- [ ] `trouble-01-imagepullbackoff.png`: isolated Pod in `ImagePullBackOff`.
- [ ] `trouble-02-image-diagnosis.png`: `describe`/events reveal nonexistent image or tag.
- [ ] `trouble-03-image-recovered.png`: corrected workload Running or fault resource removed.

### Broken Service

- [ ] `trouble-04-no-endpoints.png`: broken Service has no endpoints.
- [ ] `trouble-05-label-diagnosis.png`: Service selector and Pod labels visibly mismatch.
- [ ] `trouble-06-service-recovered.png`: corrected endpoints and successful request.

## Final documentation and presentation — M10

- [ ] Root `README.md` explains purpose, architecture, prerequisites, local run, tests, Docker, CI/CD, Terraform, Kubernetes/Helm, monitoring, troubleshooting, cost control, and cleanup.
- [ ] Presentation slide/runbook maps sections to M1–M10.
- [ ] Live/recorded demo begins with the working application and incident CRUD.
- [ ] Show Swagger and database table.
- [ ] Commit a small, prepared change with a meaningful message.
- [ ] Show the push starting CI; show tests, builds, Trivy, and SHA-tagged GHCR images.
- [ ] Show deployment update to the same SHA and healthy rollout.
- [ ] Show Terraform/AWS, Pods, Services, Helm release, Ingress, HPA, Prometheus, and Grafana.
- [ ] Perform one failure simulation, diagnose it, and recover.
- [ ] End with successful `terraform destroy` evidence and cost-cleanup statement.
- [ ] Keep a backup recording in case live network/AWS behavior fails.

## URLs to submit

- [ ] GitHub repository URL.
- [ ] Successful GitHub Actions run URL.
- [ ] GHCR backend package URL.
- [ ] GHCR frontend package URL.
- [ ] Ingress/LoadBalancer application URL used during demonstration, if still available at evaluation time.
- [ ] Recording URL if remote or permitted.

## Final evidence audit

- [ ] Every M1–M10 criterion has a source file, a passing verification, and required evidence.
- [ ] Screenshots are readable and correspond to the final commit.
- [ ] No screenshot exposes a secret or sensitive account information.
- [ ] Every link opens for the grader without requesting unauthorized access.
- [ ] AWS destroy proof is the final cloud artifact.
- [ ] Submission is completed before the deadline.
