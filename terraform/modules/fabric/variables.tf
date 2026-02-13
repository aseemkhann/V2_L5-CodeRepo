terraform {
  required_providers {
    ndfc = {
      source  = "CiscoDevNet/ndfc"
      version = "0.3.0"
    }
  }
}

variable "fabric_name" {
  description = "Name of the fabric"
  type        = string
  default     = "fabric-terraform"
}

variable "site1-spine1" {
  description = "Site1 Spine1 IP address"
  type        = string
  default     = "10.15.5.11"
}

variable "site1-leaf1" {
  description = "Site1 Leaf1 IP address"
  type        = string
  default     = "10.15.5.12"
}

variable "site1-leaf1-serial" {
  description = "Site1 Leaf1 Serial Number"
  type        = string
  default     = "97YQPYE9NLN"
}

variable "site1-leaf2" {
  description = "Site1 Leaf2 IP address"
  type        = string
  default     = "10.15.5.13"
}

variable "site1-leaf2-serial" {
  description = "Site1 Leaf2 Serial Number"
  type        = string
  default     = "90K5CH5NU1U"
}

