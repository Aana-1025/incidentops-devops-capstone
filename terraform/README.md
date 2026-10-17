# IncidentOps Terraform

This root module defines the short-lived AWS infrastructure used for the IncidentOps grading demonstration. It uses direct Terraform resources so the VPC, networking, IAM, EKS cluster, node group, Pod Identity, and storage support remain easy to inspect and explain.

```text
Internet
   |
Internet Gateway
   |
IncidentOps VPC 10.0.0.0/16
   |
+----------------------+----------------------+
| Public Subnet A      | Public Subnet B      |
+----------------------+----------------------+
                  |
              EKS cluster
        public /32 + private endpoint
                  |
       Managed node group (1-2 nodes)
```

The two public subnets are selected from different available Availability Zones. Nodes receive public addresses and use the Internet Gateway directly, avoiding NAT Gateway hourly and data-processing charges. This is a cost-conscious academic design, not a production networking reference.

## Reproducing the infrastructure safely

AWS resources are chargeable. Use a non-root AWS identity, confirm current EKS support and pricing, and obtain explicit approval before any future apply or destroy.

Copy `terraform.tfvars.example` to an ignored `terraform.tfvars`. Replace the documentation-only EKS API CIDR with the operator's current public IPv4 address followed by `/32`. Never use `0.0.0.0/0`, and never put AWS credentials in Terraform files.

Safe initialization and validation:

```powershell
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

With an approved non-root AWS profile, a reviewed plan can be generated explicitly:

```powershell
$env:AWS_PROFILE = "your-approved-profile"
terraform -chdir=terraform plan -out=incidentops.tfplan
terraform -chdir=terraform show incidentops.tfplan
```

Plan files, local state, `.terraform/`, kubeconfig, and real `.tfvars` files are ignored. A plan must be rejected if it broadens the EKS endpoint to `0.0.0.0/0`, replaces unexpected resources, or adds NAT Gateway, RDS, ElastiCache, Elastic IP, Route 53, standalone EC2, or an AWS Load Balancer.

Applying or destroying infrastructure requires separate explicit approval in the interaction where that action occurs. A budget alert is delayed and is not a spending cap; prompt teardown is the primary cost control.

## Verified evidence run

I completed one timeboxed evidence deployment and cleanup with the following verified result:

- Region: `ap-south-1`.
- Initial plan: **21 add, 0 change, 0 destroy**.
- One dedicated VPC and two public subnets in separate Availability Zones.
- Amazon EKS version 1.36.
- Public API endpoint restricted to one current operator `/32` plus private endpoint access.
- One on-demand `t3.medium` managed node target with min/desired/max 1/1/2 and a 20 GiB node disk.
- EKS Pod Identity Agent, EBS CSI add-on, and EBS CSI Pod Identity association.
- EKS cluster and node group became Active; the worker became Ready.
- IncidentOps deployed successfully with Helm, and the EBS-backed PostgreSQL PVC worked.
- Application, API, Ingress, storage, and Kubernetes evidence were captured.
- Kubernetes application resources and the dynamically provisioned data volume were removed before infrastructure teardown.
- Terraform destroy completed: **0 added, 0 changed, 21 destroyed**.
- `terraform state list` was empty after cleanup.

No IncidentOps EKS cluster, VPC, worker, load balancer, NAT Gateway, RDS database, Elastic IP, or application data volume from that evidence session is still running.

## Managed resources

The module manages:

- VPC, Internet Gateway, two public subnets, public route table, route, and associations.
- EKS cluster and one managed node group.
- Cluster, node, and EBS CSI IAM roles plus their required policy attachments.
- EKS Pod Identity Agent.
- EBS CSI driver.
- EBS CSI Pod Identity association.

The module intentionally manages no application workload. Kubernetes resources are installed separately with Helm after the cluster is ready.

## Deployment compatibility

- Public GHCR images and existing resource requests work on EKS without registry credentials.
- The EBS CSI add-on and Pod Identity role support the PostgreSQL `ReadWriteOnce` PVC.
- Metrics Server is required before relying on the backend HPA.
- NGINX Ingress can be installed without creating an AWS Load Balancer when access is provided through controlled port-forwarding during evidence capture.
- The single `t3.medium` target is intentionally conservative; a full monitoring stack should be sized separately before any future cloud use.
- Helm deployments must use an immutable image SHA and replace the classroom-only PostgreSQL password through a secure runtime value.

## Credential and state safety

Never commit:

- AWS access keys or STS tokens.
- `terraform.tfstate` or its backups.
- Binary plans.
- Real `terraform.tfvars` values or a personal IP address.
- Kubeconfig content.
- Kubernetes Secret values.

The local state and backups from the completed evidence run are retained only as ignored historical records. They are not part of the public submission.
