resource "ndfc_vrfs" "nac_vrfs_1" {
  fabric_name            = var.fabric_name
  vrfs = {
    "NAC_TF_VRF1" = {
      vrf_template                   = "Default_VRF_Universal"
      vrf_extension_template         = "Default_VRF_Extension_Universal"
      vrf_id                         = 50000
      vlan_id                        = 1500
      vlan_name                      = "VLAN1500"
      interface_description          = "Configured using Terraform"
      vrf_description                = "Configured using Terraform"
      mtu                            = 9200
      loopback_routing_tag           = 11111
      redistribute_direct_route_map  = "FABRIC-RMAP-REDIST"
      max_bgp_paths                  = 2
      max_ibgp_paths                 = 3
      ipv6_link_local                = false
      no_rp                          = false
      rp_external                    = true
      overlay_multicast_groups       = "234.0.0.0/8"
      mvpn_inter_as                  = false
      trm_bgw_msite                  = true
      advertise_host_routes          = true
      advertise_default_route        = false
      configure_static_default_route = false
      bgp_password                   = "1234567890ABCDEF"
      bgp_password_type              = "7"
      netflow                        = false
      netflow_monitor                = "MON1"
      disable_rt_auto                = true
      route_target_import            = "1:1"
      route_target_export            = "1:1"
      route_target_import_evpn       = "1:1"
      route_target_export_evpn       = "1:1"
      route_target_import_cloud_evpn = "1:1"
      route_target_export_cloud_evpn = "1:1"
      attach_list = {
        (var.site1-leaf1-serial) = {
          vlan                   = 1500
          loopback_id            = 105
          loopback_ipv4          = "1.2.3.4"
          loopback_ipv6          = "2001::1"
          deploy_this_attachment = false
        }
        (var.site1-leaf2-serial) = {
          vlan                   = 1501
          loopback_id            = 106
          loopback_ipv4          = "1.2.3.4"
          loopback_ipv6          = "2001::1"
          deploy_this_attachment = false
        }
      }

    }
  }

  depends_on = [
    ndfc_interface_ethernet.nac_interface_ethernet_1,
    ndfc_interface_loopback.nac_interface_loopback_1,
    ndfc_interface_portchannel.nac_interface_portchannel_1,
  ]
}

