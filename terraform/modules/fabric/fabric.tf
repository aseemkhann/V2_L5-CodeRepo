resource "ndfc_fabric_vxlan_evpn" "nac_fabric1" {
  fabric_name                                 = var.fabric_name
  anycast_gw_mac                              = "2020.0000.00aa"
  grfield_debug_flag                          = "Enable"
  bgp_as                                      = "65000"
  ospf_area_id                                = "0.0.0.0"
  ospf_auth_enable                            = false
  overlay_mode                                = "cli"
  deploy                                      = false
}
