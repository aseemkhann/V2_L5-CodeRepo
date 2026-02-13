resource "ndfc_interface_loopback" "nac_interface_loopback_1" {
  policy        = "int_loopback"
  deploy        = false
  serial_number = var.site1-leaf1-serial
  interfaces = {
    "Loopback100" = {
      interface_name        = "loopback100"
      admin_state           = false
      interface_description = "Configured using Terraform"
      vrf                   = "default"
      ipv4_address          = "192.168.20.1"
      ipv6_address          = "2002:db8::1"
      route_map_tag         = "100"
    }
    "Loopback101" = {
      interface_name        = "loopback101"
      admin_state           = false
      interface_description = "Configured using Terraform"
      vrf                   = "default"
      ipv4_address          = "192.168.21.1"
      ipv6_address          = "2002:db8::1"
      route_map_tag         = "100"
    }
    "Loopback102" = {
      interface_name        = "loopback102"
      admin_state           = false
      interface_description = "Configured using Terraform"
      vrf                   = "default"
      ipv4_address          = "192.168.22.1"
      ipv6_address          = "2002:db8::1"
      route_map_tag         = "100"
    }
  }

  depends_on = [
    ndfc_inventory_devices.nac_inventory_devices_1,
  ]
}

resource "ndfc_interface_ethernet" "nac_interface_ethernet_1" {
  policy        = "int_access_host"
  policy_type   = "system"
  deploy        = false
  serial_number = var.site1-leaf1-serial
  interfaces = {
    "Ethernet1/20" = {
      interface_name        = "Ethernet1/20"
      freeform_config       = "delay 200"
      admin_state           = true
      interface_description = "Configured using Terraform"
      bpdu_guard            = "true"
      port_type_fast        = false
      mtu                   = "default"
      speed                 = "Auto"
      access_vlan           = 55
      orphan_port           = false
      ptp                   = false
      netflow               = false
      netflow_monitor       = "MON1"
      netflow_sampler       = "SAMPLER1"
      allowed_vlans         = "10-20"
      native_vlan           = 1
    }
  }

  depends_on = [
    ndfc_inventory_devices.nac_inventory_devices_1,
  ]
}

resource "ndfc_interface_portchannel" "nac_interface_portchannel_1" {
  policy        = "int_port_channel_trunk_host"
  deploy        = false
  serial_number = var.site1-leaf1-serial
  interfaces = {
    "Port-channel100" = {
      interface_name        = "port-channel100"
      admin_state           = false
      interface_description = "Configured using Terraform"
      bpdu_guard            = "true"
      port_type_fast        = false
      mtu                   = "default"
      speed                 = "Auto"
      orphan_port           = false
      netflow               = false
      netflow_monitor       = "MON1"
      netflow_sampler       = "SAMPLER1"
      allowed_vlans         = "10-20"
      native_vlan           = 1
      copy_po_description   = false
      portchannel_mode      = "on"
      member_interfaces     = "eth1/12-14"
    }
  }

  depends_on = [
    ndfc_inventory_devices.nac_inventory_devices_1,
  ]
}
