# IncidentOps Submission Evidence

I kept the detailed grading evidence in this directory so each part of the DevOps pipeline can be checked without making the main README too long. It contains only screenshots and raw terminal output that demonstrate a rubric requirement. The original, unredacted capture archive remains outside the repository in `C:\Users\hp\Desktop\IncidentOps-Evidence`.

Sensitive identifiers and the worker public IP are redacted in the repository copies. The redactions do not hide the configuration or result being assessed.

## Evidence baseline

- Reviewed documentation baseline before M10: `d1986022749fcb8fe6c15d2daddf85effe1d7b3d`
- Final M10 application release: `2b76fa3c3b1c580fe48d4b3b5504c4206793061d`
- Immutable application image used for the AWS demonstration: `027054b156149f0f729380ae34e9bc4c3532fdcf`
- Initial Terraform provisioning plan: **21 add, 0 change, 0 destroy**
- Final Terraform destruction: **0 add, 0 change, 21 destroy**
- AWS region: `ap-south-1`

## Evidence map

| Milestone | What the evidence proves | Relevant SHA | Files |
| --- | --- | --- | --- |
| M1 — Application | The responsive IncidentOps dashboard and its empty state render correctly. The final M10 walkthrough also verified a populated live dashboard. | `85b40da`; `2b76fa3` | [`m1-01-dashboard.png`](M1-application/m1-01-dashboard.png), [`M10 demonstration record`](M10-demo/README.md) |
| M2 — Testing | All 16 backend API tests passed. | `85b40da` | [`m2-01-pytest-16-passed.png`](M2-testing/m2-01-pytest-16-passed.png) |
| M3 — Git | The repository had 14 meaningful Conventional Commit milestones at capture time and 19 before the final documentation commit. | `1553a22` at capture; `2b76fa3` M10 release | [`m3-01-git-history.png`](M3-git/m3-01-git-history.png) |
| M4 — Docker | Compose built the stack, all services became healthy, and application containers ran as non-root. | `4fb0fff` | [`m4-01-compose-build.png`](M4-docker/m4-01-compose-build.png), [`m4-02-compose-healthy.png`](M4-docker/m4-02-compose-healthy.png), [`m4-03-non-root.png`](M4-docker/m4-03-non-root.png) |
| M5 — CI/CD | GitHub Actions passed the quality and container security jobs, then published immutable backend and frontend images to GHCR. The detailed job captures are from the first CI milestone; the overview and package captures also show the later baseline. | `34ed129`; `85b40da` | [`m5-01-actions-green.png`](M5-cicd/m5-01-actions-green.png), [`m5-02-quality-job.png`](M5-cicd/m5-02-quality-job.png), [`m5-03-build-scan-publish.png`](M5-cicd/m5-03-build-scan-publish.png), [`m5-04-ghcr-backend.png`](M5-cicd/m5-04-ghcr-backend.png), [`m5-05-ghcr-frontend.png`](M5-cicd/m5-05-ghcr-frontend.png) |
| M6 — Trivy | The backend image at the first CI SHA and the frontend image at the final baseline had no HIGH or CRITICAL findings. | `34ed129`; `85b40da` | [`m6-01-backend-clean.png`](M6-trivy/m6-01-backend-clean.png), [`m6-02-frontend-clean.png`](M6-trivy/m6-02-frontend-clean.png) |
| M7 — Terraform and AWS | The real plan was 21/0/0; Terraform created the intended VPC, two public subnets, EKS 1.36 cluster, and `t3.medium` node; Kubernetes saw the node as Ready; the environment was later destroyed and Terraform reported 0/0/21. | `027054b`; `85b40da` baseline | [`m7-01-plan-summary.png`](M7-terraform-aws/m7-01-plan-summary.png), [`m7-02-vpc.png`](M7-terraform-aws/m7-02-vpc.png), [`m7-03-public-subnets.png`](M7-terraform-aws/m7-03-public-subnets.png), [`m7-04-eks-active.png`](M7-terraform-aws/m7-04-eks-active.png), [`m7-05-node-group-active.png`](M7-terraform-aws/m7-05-node-group-active.png), [`m7-06-node-ready.png`](M7-terraform-aws/m7-06-node-ready.png), [`m7-07-destroy-complete.png`](M7-terraform-aws/m7-07-destroy-complete.png), [`terraform-original-plan-output.txt`](M7-terraform-aws/terraform-original-plan-output.txt), [`terraform-destroy-output.txt`](M7-terraform-aws/terraform-destroy-output.txt) |
| M8 — Kubernetes and Helm | The AWS deployment ran two backend replicas, two frontend replicas, PostgreSQL with a bound EBS PVC, Helm, Ingress, API routing, HPA scaling, and two recovery exercises. The AWS application used image SHA `027054b`; HPA and troubleshooting exercises were also verified locally. | `027054b`; Helm baseline `85b40da` | [`m8-01-pods-running.png`](M8-kubernetes-helm/m8-01-pods-running.png), [`m8-02-services.png`](M8-kubernetes-helm/m8-02-services.png), [`m8-03-helm-release.png`](M8-kubernetes-helm/m8-03-helm-release.png), [`m8-04-ingress.png`](M8-kubernetes-helm/m8-04-ingress.png), [`m8-05-pvc-bound.png`](M8-kubernetes-helm/m8-05-pvc-bound.png), [`m8-06-browser-app.png`](M8-kubernetes-helm/m8-06-browser-app.png), [`m8-07-api-through-ingress.png`](M8-kubernetes-helm/m8-07-api-through-ingress.png), [`m8-08-hpa-baseline.png`](M8-kubernetes-helm/m8-08-hpa-baseline.png), [`m8-09-hpa-scale-to-five.png`](M8-kubernetes-helm/m8-09-hpa-scale-to-five.png), [`m8-10-imagepullbackoff.png`](M8-kubernetes-helm/m8-10-imagepullbackoff.png), [`m8-11-wrong-target-port.png`](M8-kubernetes-helm/m8-11-wrong-target-port.png) |
| M9 — Observability | FastAPI exposed Prometheus metrics, Prometheus scraped a healthy target, Grafana displayed the IncidentOps dashboard, and the monitoring workloads were healthy. This monitoring proof was captured locally. | `1fc0931`; `85b40da` baseline | [`m9-01-metrics.png`](M9-observability/m9-01-metrics.png), [`m9-02-prometheus-targets-up.png`](M9-observability/m9-02-prometheus-targets-up.png), [`m9-03-grafana-dashboard.png`](M9-observability/m9-03-grafana-dashboard.png), [`m9-04-monitoring-pods.png`](M9-observability/m9-04-monitoring-pods.png) |
| M10 — Final demo | A visible SLA-policy change flowed through a successful pipeline, clean Trivy gates, immutable GHCR images, and a local Helm upgrade. The exact deployed SHA, rollout, browser/API checks, CRUD lifecycle, and PostgreSQL persistence were verified. | `2b76fa3` | [`M10 demonstration record`](M10-demo/README.md), [`Helm upgrade output`](M10-demo/m10-04-helm-upgrade.txt), [`rollout and SHA output`](M10-demo/m10-05-rollout-sha.txt) |

## Review notes

The terminal text files in M7 are copied from genuine captured Terraform output; they were not recreated after teardown. The evidence intentionally shows both successful behavior and recovery from injected failures. No credentials, Terraform state, plan binaries, kubeconfig, or secret values belong in this directory.
