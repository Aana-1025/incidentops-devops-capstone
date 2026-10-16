locals {
  name_prefix = "${var.project_name}-${var.environment}"
  cluster_name = coalesce(
    var.cluster_name,
    "${local.name_prefix}-eks"
  )

  common_tags = merge(
    {
      Project     = "IncidentOps"
      ManagedBy   = "Terraform"
      Environment = var.environment
    },
    var.additional_tags
  )

  public_subnets = {
    for index, cidr in var.public_subnet_cidrs :
    data.aws_availability_zones.available.names[index] => cidr
  }
}
