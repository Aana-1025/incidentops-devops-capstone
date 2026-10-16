variable "region" {
  description = "AWS region in which to create the short-lived demo infrastructure."
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = length(trimspace(var.region)) > 0
    error_message = "region must not be empty."
  }
}

variable "project_name" {
  description = "Lowercase project identifier used in names and tags."
  type        = string
  default     = "incidentops"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,23}$", var.project_name))
    error_message = "project_name must be 3-24 lowercase letters, numbers, or hyphens and start with a letter."
  }
}

variable "environment" {
  description = "Environment label used in names and tags."
  type        = string
  default     = "demo"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,15}$", var.environment))
    error_message = "environment must be 2-16 lowercase letters, numbers, or hyphens and start with a letter."
  }
}

variable "cluster_name" {
  description = "Optional EKS cluster name. Null derives incidentops-demo-eks from project and environment."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition     = var.cluster_name == null || can(regex("^[0-9A-Za-z][0-9A-Za-z_-]{0,99}$", var.cluster_name))
    error_message = "cluster_name must use only letters, numbers, hyphens, or underscores."
  }
}

variable "kubernetes_version" {
  description = "Optional supported EKS minor version such as 1.37. Null asks EKS to use its current default."
  type        = string
  default     = null
  nullable    = true

  validation {
    condition     = var.kubernetes_version == null || can(regex("^1\\.[0-9]{2}$", var.kubernetes_version))
    error_message = "kubernetes_version must be null or an EKS minor version such as 1.37."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the dedicated IncidentOps VPC."
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr must be a valid IPv4 CIDR."
  }
}

variable "public_subnet_cidrs" {
  description = "At least two distinct public subnet CIDRs, assigned across available AZs."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]

  validation {
    condition = (
      length(var.public_subnet_cidrs) >= 2 &&
      length(distinct(var.public_subnet_cidrs)) == length(var.public_subnet_cidrs) &&
      alltrue([for cidr in var.public_subnet_cidrs : can(cidrnetmask(cidr))])
    )
    error_message = "public_subnet_cidrs must contain at least two distinct valid IPv4 CIDRs."
  }
}

variable "cluster_endpoint_public_access_cidrs" {
  description = "Trusted operator CIDRs allowed to reach the public EKS API. Replace the documentation address before planning."
  type        = list(string)

  validation {
    condition = (
      length(var.cluster_endpoint_public_access_cidrs) > 0 &&
      !contains(var.cluster_endpoint_public_access_cidrs, "0.0.0.0/0") &&
      alltrue([for cidr in var.cluster_endpoint_public_access_cidrs : can(cidrnetmask(cidr))])
    )
    error_message = "Provide at least one valid trusted CIDR; unrestricted 0.0.0.0/0 access is not allowed."
  }
}

variable "node_instance_types" {
  description = "EC2 instance types available to the managed node group."
  type        = list(string)
  default     = ["t3.medium"]

  validation {
    condition     = length(var.node_instance_types) > 0
    error_message = "node_instance_types must contain at least one instance type."
  }
}

variable "node_capacity_type" {
  description = "Managed node group purchase model. ON_DEMAND is predictable for the short evidence window."
  type        = string
  default     = "ON_DEMAND"

  validation {
    condition     = contains(["ON_DEMAND", "SPOT"], var.node_capacity_type)
    error_message = "node_capacity_type must be ON_DEMAND or SPOT."
  }
}

variable "node_disk_size_gib" {
  description = "Root EBS volume size for each managed worker node."
  type        = number
  default     = 20

  validation {
    condition     = var.node_disk_size_gib >= 20 && var.node_disk_size_gib <= 100
    error_message = "node_disk_size_gib must be between 20 and 100 GiB."
  }
}

variable "node_min_size" {
  description = "Minimum managed worker count."
  type        = number
  default     = 1

  validation {
    condition     = var.node_min_size >= 1 && floor(var.node_min_size) == var.node_min_size
    error_message = "node_min_size must be a positive whole number."
  }
}

variable "node_desired_size" {
  description = "Desired managed worker count for the demo."
  type        = number
  default     = 1

  validation {
    condition     = var.node_desired_size >= 1 && floor(var.node_desired_size) == var.node_desired_size
    error_message = "node_desired_size must be a positive whole number."
  }
}

variable "node_max_size" {
  description = "Maximum managed worker count."
  type        = number
  default     = 2

  validation {
    condition     = var.node_max_size >= 1 && floor(var.node_max_size) == var.node_max_size
    error_message = "node_max_size must be a positive whole number."
  }
}

variable "additional_tags" {
  description = "Optional non-sensitive tags merged with the required project tags."
  type        = map(string)
  default     = {}
}
