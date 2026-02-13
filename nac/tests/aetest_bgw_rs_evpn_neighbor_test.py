from pyats import aetest
import logging
import json


logger = logging.getLogger(__name__)


class VerifyBgwBgpL2vpnEvpnNeighbors(aetest.Testcase):
    '''Testcase with Steps

    This testcase demonstrates the usage of testcase steps. Note that steps
    applies to subsections in CommonSetup and CommonCleanup as well.
    '''
    @aetest.setup
    def setup(self):
        '''Testcase Setup

        '''
        if self.parent.parameters['data']['vxlan']['fabric']['type'] == 'MSD':
            dci_deployment = self.parent.parameters['data']['vxlan']['multisite']['overlay_dci']['deployment_method']
            if 'Route_Server' in dci_deployment:
                route_servers = self.parent.parameters['data']['vxlan']['multisite']['overlay_dci']['route_server']['peers']
                self.route_servers = [route_server['ip_address'] for route_server in route_servers]
            elif 'Direct' in dci_deployment:
                pass

            bgw_roles = ["border_gateway", "border_gateway_spine"]
            inventory = self.parent.parameters['inventory'][self.parent.parameters['fabric']]
            self.bgw_switches = [
                {**switch, 'fabric': fabric_name, 'hostname': name}
                for fabric_name, fabric_switches in inventory.items()
                for name, switch in fabric_switches.items()
                if switch.get("role") in bgw_roles
            ]

            self.spine_counts = {
                fabric: sum(1 for switch in switches.values() if 'spine' in switch['role'])
                for fabric, switches in inventory.items()
            }

            self.leaf_counts = {
                fabric: sum(1 for switch in switches.values() if switch['role'] in ['leaf', 'border', 'border_gateway'])
                for fabric, switches in inventory.items()
            }

    @aetest.test
    def test(self, testbed, steps):
        '''Steps must pass, unless otherwise indicated

        If step fails, by default, all remaining steps are not run.
        If an assertionError is caught, it is considered Failed() instead of
        Errored().
        '''
        command = "show bgp l2vpn evpn neighbors | json"
        api = "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/execute/show"

        for switch in self.bgw_switches:
            with steps.start(f"Verify BGP EVPN neighbors for BGW {switch['hostname']}", continue_=True) as step:

                # Execute show command via Nexus Dashboard API
                payload = {"cliCommandList": [command], "ipAddress": switch['ip']}
                response = testbed.devices[self.parent.parameters['fabric']].rest.post(api, json.dumps(payload))
                output = json.loads(response[0]['response'])

                # Handle cases where TABLE_neighbor or ROW_neighbor might not exist or be empty
                if 'TABLE_neighbor' not in output or 'ROW_neighbor' not in output['TABLE_neighbor']:
                    logger.error(f"No BGP EVPN neighbor data found on {switch['hostname']}")
                    step.failed(f"No BGP EVPN neighbor data found on {switch['hostname']}")
                    continue

                # Normalize to list (could be single dict or list of dicts)
                neighbors = output['TABLE_neighbor']['ROW_neighbor']
                neighbors = neighbors if isinstance(neighbors, list) else [neighbors]

                # Get actual neighbors for switch that should match data model
                established_neighbors = [
                    neighbor
                    for neighbor in neighbors
                    if (neighbor['state'] == 'Established') and neighbor['neighbor'] in self.route_servers
                ]

                # Get established neighbors count that should match data model
                established_count = len(established_neighbors)

                # Get expected neighbors count for switch
                expected_count = len(self.route_servers)

                # Results
                if established_count == expected_count:
                    logger.info(f" ✓ Switch {switch['hostname']} has the expected {expected_count} BGP L2VPN EVPN neighbors.")
                else:
                    logger.error(f" ✗ Switch {switch['hostname']} expected {expected_count} BGP L2VPN EVPN neighbors, but had {established_count} neighbors.")
                    step.failed()


