terraform {
  required_providers {
    ndfc = {
      source  = "CiscoDevNet/ndfc"
      version = "0.3.0"
    }
  }
}

provider "ndfc" {
  url      =  "https://10.15.0.23"
  username = "admin"
  password = "cisco.123"
  insecure = true
}
