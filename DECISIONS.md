# IncidentOps Architecture Decision Log

Status vocabulary: **Accepted**, **Proposed**, **Deferred**, **Rejected**.

## ADR-001 — Build IncidentOps, not a TaskBoard variant

**Status:** Accepted

**Decision:** The product domain is cloud incident and service reliability management. Its entities, terminology, workflows, UI copy, dashboard, API routes, and branding will be original.

**Why:** The domain is relevant to DevOps/SRE and demonstrates a coherent reason for health checks, metrics, alerts, autoscaling, and troubleshooting. It also satisfies the plagiarism rule that a direct TaskBoard clone receives zero.

**Consequence:** We may reuse general architecture patterns, but no Task model, TaskBoard UI, sample names, or copied application code.

## ADR-002 — Keep the product scope small but demonstrable

**Status:** Accepted

**Decision:** Initial product scope is Services plus Incidents, full incident CRUD/lifecycle, dashboard statistics, and a derived SLA-risk indicator.

**Why:** This is enough to show a realistic product and multiple API behaviors while leaving time for the DevOps layers that carry most marks.

**Not included initially:** authentication/RBAC, email/SMS/pager integrations, WebSockets, comments, attachments, audit-event service, microservices, message queues, AI incident summaries, multi-tenancy, mobile apps, and advanced SLA policy engines.

## ADR-003 — Use FastAPI, SQLAlchemy, Alembic, and PostgreSQL

**Status:** Accepted

**Decision:** Backend uses FastAPI, Pydantic, SQLAlchemy 2.x, Alembic, and PostgreSQL.

**Why:** This matches the course's expected stack, offers clear Swagger documentation and validation, makes CRUD/test demonstrations straightforward, and shows professional migration/database practices.

**Consequence:** Schema creation in application startup will not replace migrations in production. Readiness must execute a safe database check.

## ADR-004 — Use React and Vite for a responsive operations UI

**Status:** Accepted

**Decision:** Build a custom React/Vite single-page dashboard with plain CSS or a free lightweight styling approach.

**Why:** Vite is fast, React is resume-relevant, and a custom responsive interface meets the rubric without paid design systems.

**Consequence:** The UI must include useful loading/error/empty states and real API calls, not static mock cards.

## ADR-005 — Develop and verify locally before AWS

**Status:** Accepted

**Decision:** Application, tests, images, Compose, Helm, HPA, monitoring, and troubleshooting are proven locally before AWS resources are created.

**Why:** Local iteration is faster, repeatable, nearly free, and reduces the paid EKS window and demo risk.

**Consequence:** AWS is not used as a debugging environment. The EKS session begins only after a complete local rehearsal.

## ADR-006 — Use free tooling everywhere except the required AWS evidence

**Status:** Accepted

**Decision:** Use free/open-source local tools and free GitHub capabilities: Git, GitHub public repository, GitHub Actions allowance, GHCR allowance, Docker tooling, PostgreSQL, Pytest, Trivy, Terraform, Kubernetes/kind or Docker Desktop, Helm, NGINX Ingress, Prometheus, and Grafana. AWS is the explicit spending exception.

**Why:** This follows the stated budget while still targeting all rubric sections.

**Consequence:** No paid SaaS monitoring, CI, container registry, design assets, domain, TLS certificate, database, or notification service is planned.

## ADR-007 — Control AWS cost through timeboxing and teardown

**Status:** Accepted

**Decision:** The AWS deployment is a short, pre-rehearsed evidence window with explicit apply approval and same-session destroy.

**Controls:**

- Set AWS Budget alerts before apply; monitoring alerts are free, but they are delayed and are not a hard cap.
- Recheck current prices, region, quotas, and supported EKS version immediately before use.
- Use one EKS cluster and one minimal managed worker group.
- Avoid RDS, Route 53 domain purchase, paid TLS, and optional managed services.
- Prefer local monitoring rehearsal; run cloud monitoring only long enough for proof.
- Avoid NAT Gateway if a rubric-compliant, rehearsed public-subnet node design is safe and workable; if NAT is required, use one and destroy promptly.
- Tag resources with `Project=IncidentOps`, `Environment=grading`, and an owner identifier for discovery and cleanup.
- Prepare all screenshots/commands before apply.
- Run `terraform destroy`, verify the plan/state and AWS Console, then recheck billing later.

**Why:** EKS has a cluster-hour charge and also incurs worker, storage, IP, and networking costs. A ₹100 ceiling is very tight and cannot be guaranteed by a budget alert.

Official pricing references: [EKS](https://aws.amazon.com/eks/pricing/), [VPC/NAT Gateway](https://aws.amazon.com/vpc/pricing/), [AWS Budgets](https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/).

**Consequence:** No `terraform apply` or cloud creation occurs without the user's explicit approval. Exact cost must be estimated again before that approval.

## ADR-008 — Treat the rubric as authoritative when the sample is weaker

**Status:** Accepted

**Decision:** Meet the written grading criteria even if the teacher's reference implementation omits or misconfigures an item.

**Observed reference risks:** the inspected sample test file contains fewer than the rubric's five required tests; the sample frontend runtime does not explicitly switch to a non-root user; and its Ingress backend port does not appear to match its backend Service port.

**Consequence:** IncidentOps targets ten or more tests, proves both runtime users are non-root, and validates all rendered Service/Ingress ports and selectors.

## ADR-009 — Use a modular monolith, not microservices

**Status:** Accepted

**Decision:** One FastAPI backend serves service and incident modules; one React frontend consumes it.

**Why:** Microservices would multiply containers, pipelines, network failure modes, and cost without earning additional rubric points.

**Consequence:** Code remains separated by routers/services internally so the project still looks professional.

## ADR-010 — Keep browser routing same-origin

**Status:** Accepted

**Decision:** The frontend calls `/api`; Nginx and Ingress route it to the backend.

**Why:** This avoids environment-specific backend URLs, simplifies CORS, and matches container/Kubernetes routing.

**Consequence:** Nginx and Ingress path behavior must be integration-tested; the backend Service port is the single source of truth.

## ADR-011 — Use immutable SHA image tags

**Status:** Accepted

**Decision:** CI publishes and Helm deploys image tags derived from the Git commit SHA. `latest` is not a deployment input.

**Why:** This is explicitly graded and provides source-to-runtime traceability and predictable rollback.

**Consequence:** Demo evidence must show the same SHA in GitHub, Actions/GHCR, and deployment values/image IDs.

## ADR-012 — Test isolation is mandatory

**Status:** Accepted

**Decision:** Pytest overrides database dependencies and uses an isolated test database/transaction strategy.

**Why:** The rubric awards two points for not touching production, and destructive CRUD tests must never risk real data.

**Consequence:** Test startup fails safely if a production-style database URL is accidentally selected.

## ADR-013 — PostgreSQL runs in-cluster only for the classroom demonstration

**Status:** Accepted

**Decision:** Use a PVC-backed PostgreSQL workload for the Kubernetes demo; use Compose locally.

**Why:** It satisfies the application architecture without adding RDS cost. A production system would usually evaluate managed RDS, backups, high availability, and secrets management.

**Consequence:** Documentation must clearly label in-cluster PostgreSQL as a capstone/demo tradeoff, not a universal production recommendation.

## ADR-014 — Provision the Grafana dashboard from source

**Status:** Accepted

**Decision:** Store dashboard definition/provisioning configuration in the repository rather than creating the only dashboard manually in the UI.

**Why:** Reproducibility strengthens the DevOps story and ensures the required populated panel can be recreated quickly.

**Consequence:** The demo still shows the live Grafana UI and generated traffic.

## ADR-015 — Separate intentional faults from the main release

**Status:** Accepted

**Decision:** Broken-image and broken-Service manifests use isolated names and labels.

**Why:** Troubleshooting can be demonstrated without taking the graded application offline or corrupting its Helm release.

**Consequence:** Recovery includes deleting/fixing the isolated exercise resources and proving the main app stayed healthy.

## ADR-016 — Derive SLA targets from severity in application code

**Status:** Accepted

**Decision:** Define the initial P1–P4 SLA target durations as an immutable application policy keyed by incident severity. Do not persist a duplicated SLA deadline or target duration on each incident.

**Why:** Severity and timestamps are the source facts needed to calculate SLA risk. A stored derived value could become stale when severity changes and would add migration and synchronization complexity without improving this capstone milestone.

**Consequence:** Future service logic calculates SLA risk from severity, creation time, current time, and resolution time. If policy later varies by service or customer, it can become a dedicated policy model through a reviewed migration.

## ADR-017 — Separate host and container PostgreSQL addresses

**Status:** Accepted

**Decision:** Publish the local Compose PostgreSQL service as `localhost:5433` while retaining PostgreSQL's standard container port `5432`. Host-run backend processes use `localhost:5433`; future Compose backend containers use the service address `postgres:5432`.

**Why:** Host port `5432` is already owned by an unrelated PostgreSQL process that must remain untouched. Docker service discovery removes the need for containers to use the published host port.

**Consequence:** Development documentation and example configuration must clearly distinguish host execution from container execution. The Compose database remains PostgreSQL-compatible without changing its internal listener.

## Decisions requiring later user review

- **AWS account and approved region:** Proposed default is the lowest-risk region compatible with the teacher's expectations; `ap-south-1` is not assumed until current cost/quota support is checked.
- **Local Kubernetes:** Docker Desktop Kubernetes or kind, based on what is installed and reliable on the user's machine.
- **AWS Ingress implementation:** NGINX plus a Service LoadBalancer versus AWS Load Balancer Controller; select after current cost and setup complexity are compared.
- **Repository visibility:** Public is simplest for grading; a private repository requires confirmed instructor access and may affect package visibility.
- **License and personal branding:** add only after the user supplies the preferred name/identity.
