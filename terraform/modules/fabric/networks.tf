resource "ndfc_networks" "nac_networks_1" {
  fabric_name            = var.fabric_name
  networks = {
    "NAC_TF_NET1" = {
      display_name               = "NAC_TF_NET1"
      network_id                 = 30001
      network_template           = "Default_Network_Universal"
      network_extension_template = "Default_Network_Extension_Universal"
      vrf_name                   = "NAC_TF_VRF1"
      primary_network_id         = 30000
      network_type               = "Normal"
      gateway_ipv4_address       = "192.0.2.1/24"
      gateway_ipv6_address       = "2001:db8::1/64"
      vlan_id                    = 1600
      vlan_name                  = "VLAN2000"
      layer2_only                = false
      interface_description      = "Configured using Terraform"
      mtu                        = 9200
      secondary_gateway_1        = "192.168.2.1/24"
      secondary_gateway_2        = "192.168.3.1/24"
      secondary_gateway_3        = "192.168.4.1/24"
      secondary_gateway_4        = "192.168.5.1/24"
      arp_suppression            = false
      ingress_replication        = false
      multicast_group            = "233.1.1.1"
      dhcp_relay_loopback_id     = 134
      routing_tag                = 11111
      route_target_both          = true
      netflow                    = false
      svi_netflow_monitor        = "MON1"
      vlan_netflow_monitor       = "MON1"
      l3_gatway_border           = true
      igmp_version               = "3"
      attachments = {
        (var.site1-leaf1-serial) = {
          vlan                   = 1600
          deploy_this_attachment = false
          switch_ports           = []
        }
        (var.site1-leaf2-serial) = {
          vlan                   = 1600
          deploy_this_attachment = false
          switch_ports           = []
        }
      }

    }

  }
  depends_on = [
    ndfc_vrfs.nac_vrfs_1,
  ]

}

resource "ndfc_networks" "nac_networks_2" {
  fabric_name            = var.fabric_name
  networks = {
    "NAC_TF_NET2" = {
      display_name               = "NAC_TF_NET2"
      network_id                 = 30002
      network_template           = "Default_Network_Universal"
      network_extension_template = "Default_Network_Extension_Universal"
      vrf_name                   = "NAC_TF_VRF1"
      primary_network_id         = 30002
      network_type               = "Normal"
      gateway_ipv4_address       = "192.0.3.1/24"
      vlan_id                    = 1601
      vlan_name                  = "VLAN2044"
      layer2_only                = false
      interface_description      = "Configured using Terraform"
      mtu                        = 9200
      arp_suppression            = false
      ingress_replication        = false
      multicast_group            = "233.1.1.1"
      dhcp_relay_loopback_id     = 134
      routing_tag                = 11111
      route_target_both          = true
      netflow                    = false
      svi_netflow_monitor        = "MON1"
      vlan_netflow_monitor       = "MON1"
      l3_gatway_border           = true
      igmp_version               = "3"
      attachments = {
        (var.site1-leaf1-serial) = {
          # vlan                   = 1601
          deploy_this_attachment = false
          switch_ports           = []
        }
        (var.site1-leaf2-serial) = {
          # vlan                   = 1601
          deploy_this_attachment = false
          switch_ports           = []
        }
      }

    }
  }
  depends_on = [
    ndfc_vrfs.nac_vrfs_1,
  ]
}
