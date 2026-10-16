# IncidentOps Terraform

This root module defines the short-lived AWS infrastructure needed for the IncidentOps grading demonstration. It uses direct resources so the VPC, networking, IAM, EKS cluster, node group, and storage support remain easy to explain.

```text
Internet
   |
Internet Gateway
   |
IncidentOps VPC
   |
+----------------------+----------------------+
| Public Subnet A      | Public Subnet B      |
+----------------------+----------------------+
                 |
             EKS cluster
                 |
        Managed node group (1-2 nodes)
```

The two public subnets are selected from different available Availability Zones. Nodes receive public IPs and use the Internet Gateway directly, avoiding NAT Gateway hourly and data-processing charges. This is a cost-conscious academic design, not a production networking reference.

## Safe local validation

Copy `terraform.tfvars.example` to an ignored `terraform.tfvars`, then replace the documentation-only EKS API CIDR with your current public IPv4 address followed by `/32`. No AWS credentials belong in either file.

```powershell
terraform -chdir=terraform fmt -recursive
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

Initialization only downloads the provider and creates the dependency lock file. Formatting and validation do not create AWS resources. A real plan requires safe external AWS authentication and belongs to the separately approved AWS evidence session:

```powershell
terraform -chdir=terraform plan -out=incidentops.tfplan
terraform -chdir=terraform show incidentops.tfplan
```

Plan files, local state, `.terraform/`, and real `.tfvars` files are ignored. Review the plan for the expected VPC, two subnets, EKS cluster, managed node group, IAM roles, EKS add-ons, and EBS volumes before considering an apply.

## Paid actions — explicit approval required

`terraform apply` creates chargeable AWS infrastructure. **Do not run it without explicit approval in that interaction.** The future evidence window may incur charges for the EKS control plane, EC2 worker nodes, EBS node/PVC volumes, and public IPv4 addresses. An Ingress controller may also create a chargeable AWS load balancer; it is deliberately outside this Terraform module.

The configuration intentionally creates no NAT Gateway, RDS/Aurora, ElastiCache, Route 53 hosted zone, Elastic IP, standalone EC2 instance, or standalone load balancer. It configures EKS standard support to avoid extended-support pricing and leaves the Kubernetes version null so EKS can choose its current default.

Immediately after all grading evidence is captured, run the destructive cleanup only with explicit approval:

```powershell
helm uninstall incidentops -n incidentops
terraform -chdir=terraform destroy
```

Verify the destroy summary, confirm the VPC/EKS resources are absent, and retain the required screenshots. AWS billing data may be delayed, so teardown—not a budget alert—is the primary cost control.

## Deployment compatibility notes

- Public GHCR images and existing CPU/memory requests work on EKS without registry credentials.
- The EBS CSI add-on and its Pod Identity role support the PostgreSQL `ReadWriteOnce` PVC. Confirm the cluster's available StorageClasses before installing IncidentOps.
- Install Metrics Server before relying on the backend HPA.
- Install an Ingress implementation deliberately. The local `nginx` class works only after NGINX Ingress is installed; AWS Load Balancer Controller is not installed by this module and would add complexity and possible load-balancer cost.
- Install kube-prometheus-stack selectively during the short evidence window because one `t3.medium` node is intentionally conservative.
- Use a current immutable image SHA in Helm values and replace the development-only PostgreSQL password through a secure runtime value.
