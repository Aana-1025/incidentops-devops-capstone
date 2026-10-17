# M10 — Final Deployment Demonstration

## Traceability

- M10 release SHA: `2b76fa3c3b1c580fe48d4b3b5504c4206793061d`
- Commit: `feat(ui): add SLA policy quick reference`
- GitHub Actions: [run #11](https://github.com/Aana-1025/incidentops-devops-capstone/actions/runs/39031611188) — successful
- Backend image: `ghcr.io/aana-1025/incidentops-backend:2b76fa3c3b1c580fe48d4b3b5504c4206793061d`
- Frontend image: `ghcr.io/aana-1025/incidentops-frontend:2b76fa3c3b1c580fe48d4b3b5504c4206793061d`

The pipeline ran all 16 backend tests, frontend lint and build, built both images, passed both Trivy HIGH/CRITICAL gates, and published both immutable SHA tags.

## Local deployment result

The demonstration used the `docker-desktop` Kubernetes context and the existing `incidentops` Helm release. Helm revision 6 deployed both the backend and frontend at the M10 release SHA. The migration Job completed, both backend replicas and both frontend replicas became Ready, and PostgreSQL remained Ready.

The browser loaded the dashboard through local NGINX Ingress, showed the live service catalog and the new SLA quick reference (P1 30 minutes, P2 2 hours, P3 8 hours, P4 24 hours). The dashboard, `/health`, `/ready`, `/api/services`, `/api/incidents`, and `/docs` all returned HTTP 200; readiness reported `READY`.

## CRUD and persistence verification

The incident submitted during browser automation did persist; the first automated page snapshot was stale rather than evidence of an application defect. Direct API verification then proved service list/create/read/update/delete and incident list/create/read/update/delete. The incident was moved from Open to Resolved and then Investigating, confirming that `resolved_at` is set and cleared with the lifecycle. Only the clearly named temporary verification service and incident were deleted.

A read-only query in the PostgreSQL Pod confirmed that the useful `Checkout API` service and `Elevated checkout latency` incident remained stored after cleanup. No application source correction was needed.

## Evidence files

- [`m10-04-helm-upgrade.txt`](m10-04-helm-upgrade.txt) — genuine Helm upgrade output for revision 6.
- [`m10-05-rollout-sha.txt`](m10-05-rollout-sha.txt) — genuine rollout, Pod readiness, migration, and immutable image output.

This final M10 deployment used local Docker Desktop Kubernetes. It did **not** recreate or modify AWS infrastructure. The earlier AWS/EKS demonstration remains separate historical evidence under `M7-terraform-aws/` and `M8-kubernetes-helm/`.

## Final GitOps supplement

The historical M10 deployment above remains the controlled manual Helm demonstration at release SHA `2b76fa3c3b1c580fe48d4b3b5504c4206793061d`. Argo CD was added afterward as a separate local supplement for the final submission walkthrough; it does not rewrite the M10 deployment history.

Argo CD `v3.5.5` runs in the `argocd` namespace on Docker Desktop. The `incidentops-gitops` Application watches this public repository, renders `helm/incidentops` with `values-gitops.yaml`, and reconciles the isolated `incidentops-gitops` namespace. It reached `Synced` and `Healthy`; both backend and frontend ran the same immutable M10 SHA, PostgreSQL was Ready, and the migration Job completed. The original `incidentops` release remained separate.

- [`m10-06-argocd-sync.txt`](m10-06-argocd-sync.txt) — genuine non-secret Application, workload, Pod, image, and namespace output.
- [`m10-07-argocd-synced.png`](m10-07-argocd-synced.png) — real local Argo CD UI showing the Application as Healthy and Synced.

Final walkthrough artifacts are under [`demo/`](../../demo/README.md).
