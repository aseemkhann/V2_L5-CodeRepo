resource "ndfc_configuration_deploy" "nac_configuration_deploy_1" {
  fabric_name    = var.fabric_name
  serial_numbers = ["ALL"]
  recalculate    = true
  always_execute = false
  deploy         = true

  depends_on = [
    ndfc_fabric_vxlan_evpn.nac_fabric1,
    ndfc_inventory_devices.nac_inventory_devices_1,
    ndfc_interface_ethernet.nac_interface_ethernet_1,
    ndfc_interface_loopback.nac_interface_loopback_1,
    ndfc_interface_portchannel.nac_interface_portchannel_1,
    ndfc_vrfs.nac_vrfs_1,
    ndfc_networks.nac_networks_1,
  ]
}
