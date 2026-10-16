output "region" {
  description = "AWS region containing the IncidentOps demo infrastructure."
  value       = var.region
}

output "vpc_id" {
  description = "ID of the dedicated IncidentOps VPC."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets used by EKS."
  value       = values(aws_subnet.public)[*].id
}

output "public_subnet_availability_zones" {
  description = "Availability Zones selected dynamically for the public subnets."
  value       = keys(aws_subnet.public)
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster."
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Public Kubernetes API endpoint."
  value       = aws_eks_cluster.main.endpoint
}

output "eks_node_group_name" {
  description = "Name of the EKS managed node group."
  value       = aws_eks_node_group.main.node_group_name
}

output "kubectl_config_command" {
  description = "Command to configure kubectl after an explicitly approved apply."
  value       = "aws eks update-kubeconfig --region ${var.region} --name ${aws_eks_cluster.main.name}"
}
