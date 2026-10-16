# Repository Guidelines

## Mission and Primary Objective

Build **IncidentOps — Cloud Incident & Service Reliability Management Platform** into a complete, reliable, resume-quality capstone that satisfies every item in the teacher's 100-point rubric. Every change must advance a documented requirement, verification need, or grading artifact. Do not remove or weaken a rubric requirement merely to simplify implementation.

## Required Reading and Source of Truth

Before starting any milestone, read the relevant sections of:

- `GRADING_REQUIREMENTS.md` — authoritative rubric and submission requirements.
- `PROJECT_PLAN.md` — milestone sequence, dependencies, and verification.
- `ARCHITECTURE.md` — approved system design and repository layout.
- `TODO.md` — current work state; check an item only after it is proven complete.
- `DECISIONS.md` — accepted scope, security, cost, and architecture decisions.
- `EVIDENCE_CHECKLIST.md` — consult whenever work will eventually require grading evidence.

If documents conflict, preserve rubric coverage and safety, then ask the user before making a material scope or architecture change.

## Application Identity and Scope

IncidentOps must remain an original incident and service reliability product. General DevOps patterns may follow the teacher's reference, but branding, data model, API concepts, frontend, copy, and business logic must be IncidentOps-specific. Never turn it into or copy code from TaskBoard.

Initial scope is Services and Incidents, incident CRUD/lifecycle, dashboard statistics, SLA-risk indicators, health/readiness/metrics endpoints, and a responsive UI. Avoid unapproved complexity such as microservices, Kafka, Redis, OAuth, payments, RDS, paid domains, AI features, or external notification systems.

## Planned Stack and Structure

- `frontend/`: React and Vite; components under `src/components/`, API helpers under `src/services/`.
- `backend/app/`: Python, FastAPI, Pydantic, SQLAlchemy, and service logic.
- `backend/tests/`: Pytest; Alembic migrations live in `backend/alembic/versions/`.
- PostgreSQL is the application database; tests use isolated data, never production.
- `.github/workflows/`: tests, builds, Trivy scans, GHCR publishing, and controlled deployment.
- `terraform/`: AWS VPC and EKS infrastructure as code.
- `k8s/` and `helm/incidentops/`: namespace bootstrap and Helm release.
- `monitoring/`, `troubleshooting/`, `scripts/`: Prometheus/Grafana, fault exercises, and repeatable helpers.

The delivery stack also includes Git, GitHub, Docker, Docker Compose, Kubernetes, Ingress, HPA, and immutable commit-SHA image tags.

## Milestone Working Protocol

For every implementation milestone:

1. Read the applicable planning and rubric sections.
2. Inspect the current repository, existing changes, and available tools before editing.
3. Work only on the requested milestone; add a dependency only when strictly necessary and report it.
4. Implement the milestone completely with maintainable, understandable code.
5. Run every relevant available formatter, lint, build, test, render, or validation check.
6. Inspect failures, fix failures caused by the change, and rerun verification.
7. Never claim a check passed unless its command actually succeeded.
8. Update `TODO.md` only for behavior that is implemented and verified. File existence alone is not completion.
9. Use `EVIDENCE_CHECKLIST.md` to prepare reproducible evidence, but never expose secrets in evidence.
10. End with a concise report listing files created/changed, commands run, checks passed/failed, remaining issues, and the recommended next milestone.

At the current planning stage, do not implement application code, initialize Git, create frontend/backend scaffolding, or push to GitHub until the user explicitly requests the corresponding milestone.

## Build, Test, and Validation Commands

Use commands only after their files/tools exist:

```powershell
docker compose up --build
cd backend; pytest -v
cd backend; alembic upgrade head
cd frontend; npm run lint
cd frontend; npm run build
helm lint .\helm\incidentops
helm template incidentops .\helm\incidentops -n incidentops
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
```

Prefer local development, Compose, and local Kubernetes verification before AWS.

## Coding and Quality Standards

Use four spaces, type hints, PEP 8, and Ruff when configured for Python. Use two spaces in JavaScript, JSX, JSON, and YAML. React components use `PascalCase`; hooks/functions use `camelCase`; Python names use `snake_case`; Kubernetes resources use lowercase kebab-case such as `incidentops-backend`.

Keep API routers thin, validate inputs with Pydantic, and place reusable business logic in service modules. Maintain clear naming, a simple modular-monolith architecture, responsive UI states, explicit liveness/readiness behavior, reproducible environments, and non-root runtime containers.

## Testing Rules

Use Pytest with an overridden dependency and isolated SQLite or dedicated ephemeral test database. Tests must never connect to production PostgreSQL. Name files `test_*.py` and tests `test_<behavior>`. Cover health/readiness, validation, incident CRUD, statistics, resolution timestamps, service linkage, 404s, and failure paths. Target at least ten meaningful backend tests across three or more endpoints. Tests and the frontend production build must pass before container publication.

## Git and Pull Request Rules

When Git is eventually initialized:

- Use focused, meaningful Conventional Commit-style messages such as `feat(api): add incident lifecycle` or `test(api): reject invalid severity`.
- Never use vague messages such as `update`, `fix`, `changes`, or `final`, and never push broken code merely to increase commit count.
- Review `git status` and relevant diffs before committing.
- Never force-push or rewrite shared history without explicit approval.
- Keep milestone commits natural so the final history contains at least ten meaningful checkpoints.

Pull requests must explain the change, verification performed, rubric impact, linked issue where applicable, and security/cost implications. Include UI screenshots or terminal evidence for behavioral changes. Do not merge failing CI or unresolved HIGH/CRITICAL Trivy findings.

## Security and Configuration

Never expose credentials, print secrets unnecessarily, hardcode real passwords, or commit `.env`, AWS credentials, access tokens, private keys, kubeconfig, Terraform state/plan files, or real secret values. Use `.env.example`, placeholders, environment variables, and GitHub Secrets. Confirm ignored files are not tracked and keep screenshots free of sensitive data.

Use least-privilege workflow permissions, non-root images, and SHA-tagged images instead of `latest`. Treat any credential found in source or history as a release blocker.

## AWS Cost Safety — Critical

The target AWS spend is approximately **₹100**. Never run `terraform apply`, `terraform destroy`, or any command/API/UI automation that creates, modifies, or deletes real AWS infrastructure without the user's explicit approval in that exact interaction. Prior approval does not carry forward.

Non-destructive preparation such as `terraform fmt` and `terraform validate` is allowed when relevant. Run `terraform plan` only when instructed and credentials/configuration are safely available. Never create AWS resources through CLI or console automation implicitly.

Rehearse locally first. Before an approved AWS session, recheck current pricing, region, quotas, and Kubernetes support; prepare evidence; use one minimal tagged EKS environment; then destroy it in the approved session and verify cleanup. AWS Budget alerts are delayed and are not a spending cap.

## Destructive Action Safety

Do not delete or overwrite user work, rewrite Git history, affect Docker resources unrelated to IncidentOps, alter files outside this project, or modify user/cloud data without explicit permission. Resolve exact targets first and prefer recoverable operations. Preserve unrelated local changes.

## Definition of Done

A milestone is complete only when its behavior is implemented, relevant local checks succeed, rubric coverage is preserved, documentation/TODO state is accurate, and required evidence can be reproduced. If an external dependency prevents verification, report the exact limitation and leave the item incomplete.
