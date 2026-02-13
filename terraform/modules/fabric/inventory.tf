resource "ndfc_inventory_devices" "nac_inventory_devices_1" {
  fabric_name                               = var.fabric_name
  auth_protocol                             = "md5"
  username                                  = "admin"
  password                                  = "cisco.123"
  max_hops                                  = 0
  set_as_individual_device_write_credential = false
  preserve_config                           = false
  save                                      = true
  deploy                                    = false
  retries                                   = 350
  retry_wait_timeout                        = 20
  devices = {
    (var.site1-spine1) = {
      role                    = "spine"
      discovery_type          = "discover"
      discovery_auth_protocol = "md5"
    }
    (var.site1-leaf1) = {
      role                    = "leaf"
      discovery_type          = "discover"
      discovery_auth_protocol = "md5"
    }
    (var.site1-leaf2) = {
      role                    = "leaf"
      discovery_type          = "discover"
      discovery_auth_protocol = "md5"
    }
  }

  depends_on = [
    ndfc_fabric_vxlan_evpn.nac_fabric1,
  ]
}
