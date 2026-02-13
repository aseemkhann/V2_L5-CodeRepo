from pyats import aetest
import logging
import json


logger = logging.getLogger(__name__)


class VerifyNveVnis(aetest.Testcase):
    '''Testcase to verify NVE VNI status on switches

    This testcase verifies that VRFs and Networks configured in the data model through
    Nexus Dashboard are properly configured on switches and that their VNIs are in UP state.
    '''
    @aetest.setup
    def setup(self, testbed):
        '''Testcase Setup - Build VNI to switch mappings'''

        # Extract VRFs and Networks from data model
        overlay = self.parent.parameters['data']['vxlan']['multisite']['overlay']
        vrfs = overlay.get('vrfs', [])
        networks = overlay.get('networks', [])
        vrf_attach_groups = overlay.get('vrf_attach_groups', [])
        network_attach_groups = overlay.get('network_attach_groups', [])

        # Build mapping of attach group name to switch hostnames
        vrf_group_to_switches = {
            group['name']: [switch['hostname'] for switch in group.get('switches', [])]
            for group in vrf_attach_groups
        }

        network_group_to_switches = {
            group['name']: [switch['hostname'] for switch in group.get('switches', [])]
            for group in network_attach_groups
        }

        # Build mapping of switch hostname to expected VNIs
        # Structure: {hostname: [{'vni': str, 'vlan_id': int, 'type_prefix': 'L3'/'L2', 'name': str}, ...]}
        from collections import defaultdict
        switch_to_vnis = defaultdict(list)

        # Process VRFs (L3 VNIs)
        for vrf in vrfs:
            attach_group = vrf.get('vrf_attach_group')
            if attach_group and attach_group in vrf_group_to_switches:
                vni_entry = {
                    'vni': str(vrf['vrf_id']),
                    'vlan_id': vrf['vlan_id'],
                    'type_prefix': 'L3',
                    'name': vrf['name']
                }
                for hostname in vrf_group_to_switches[attach_group]:
                    switch_to_vnis[hostname].append(vni_entry)

        # Process Networks (L2 VNIs)
        for network in networks:
            attach_group = network.get('network_attach_group')
            if attach_group and attach_group in network_group_to_switches:
                vni_entry = {
                    'vni': str(network['net_id']),
                    'vlan_id': network['vlan_id'],
                    'type_prefix': 'L2',
                    'name': network['name']
                }
                for hostname in network_group_to_switches[attach_group]:
                    switch_to_vnis[hostname].append(vni_entry)

        self.switch_to_vnis = switch_to_vnis

        # Build list of switches to test (with roles: leaf, border, border_gateway, border_gateway_spine)
        target_roles = ['leaf', 'border', 'border_gateway', 'border_gateway_spine']
        inventory = self.parent.parameters['inventory'][self.parent.parameters['fabric']]

        self.test_switches = [
            {**switch, 'fabric': fabric_name, 'hostname': hostname}
            for fabric_name, fabric_switches in inventory.items()
            for hostname, switch in fabric_switches.items()
            if switch.get('role') in target_roles
        ]

        logger.info(f"Setup complete: Testing {len(self.test_switches)} switches")
        for hostname, vnis in switch_to_vnis.items():
            logger.info(f"  {hostname}: expecting {len(vnis)} VNIs")

    @aetest.test
    def test(self, testbed, steps):
        '''Verify NVE VNI status on all switches

        Steps through each switch in Nexus Dashboard inventory and verify that:
        1. All expected VNIs (from data model) are present and UP
        2. Reports any unexpected VNIs not in the data model
        '''

        command = "show nve vni | json"
        api = "/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/execute/show"

        for switch in self.test_switches:
            with steps.start(f"Verify NVE VNIs for {switch['hostname']}", continue_=True) as step:

                # Execute show command via Nexus Dashboard API
                payload = {"cliCommandList": [command], "ipAddress": switch['ip']}
                response = testbed.devices[self.parent.parameters['fabric']].rest.post(api, json.dumps(payload))
                output = json.loads(response[0]['response'])

                # Handle cases where TABLE_nve_vni or ROW_nve_vni might not exist or be empty
                if 'TABLE_nve_vni' not in output or 'ROW_nve_vni' not in output['TABLE_nve_vni']:
                    # Check if this switch should have VNIs
                    expected_vnis = self.switch_to_vnis.get(switch['hostname'], [])
                    if expected_vnis:
                        logger.error(f"No NVE VNI data found on {switch['hostname']}, but expected {len(expected_vnis)} VNIs")
                        step.failed(f"No NVE VNI data found on {switch['hostname']}, but expected {len(expected_vnis)} VNIs")
                    else:
                        logger.info(f"No NVE VNI data found on {switch['hostname']} (none expected)")
                        step.passed(f"No VNIs configured on {switch['hostname']} as expected")
                    continue

                # Normalize to list (could be single dict or list of dicts)
                actual_vnis = output['TABLE_nve_vni']['ROW_nve_vni']
                actual_vnis = actual_vnis if isinstance(actual_vnis, list) else [actual_vnis]

                # Get expected VNIs for switch
                expected_vnis = self.switch_to_vnis.get(switch['hostname'], [])
                expected_vni_numbers = {vni['vni'] for vni in expected_vnis}

                # Check each actual VNI
                actual_vni_numbers = {vni_entry.get('vni', '') for vni_entry in actual_vnis}
                expected_vni_map = {v['vni']: v for v in expected_vnis}

                # Track issues
                issues = []

                for vni_entry in actual_vnis:
                    vni_number = vni_entry.get('vni', '')
                    vni_state = vni_entry.get('vni-state', '')
                    vni_type = vni_entry.get('type', '')

                    # Check if VNI is expected
                    if vni_number not in expected_vni_numbers:
                        issues.append(f"Unexpected VNI {vni_number} found (type: {vni_type})")
                        continue

                    expected_vni = expected_vni_map[vni_number]

                    # Verify VNI state is UP
                    if vni_state != 'Up':
                        issues.append(f"VNI {vni_number} state is '{vni_state}', expected 'Up'")

                    # Verify type contains L3/L2
                    if expected_vni['type_prefix'] not in vni_type:
                        issues.append(f"VNI {vni_number} type '{vni_type}' does not contain '{expected_vni['type_prefix']}'")

                    # Verify type contains correct identifier based on VNI type
                    if expected_vni['type_prefix'] == 'L2':
                        # For L2 Networks, check for VLAN ID
                        if str(expected_vni['vlan_id']) not in vni_type:
                            issues.append(f"VNI {vni_number} type '{vni_type}' does not contain VLAN ID '{expected_vni['vlan_id']}'")
                    else:  # L3
                        # For L3 VRFs, check for VRF name (case-insensitive)
                        if expected_vni['name'].lower() not in vni_type.lower():
                            issues.append(f"VNI {vni_number} type '{vni_type}' does not contain VRF name '{expected_vni['name']}'")

                    logger.info(f"  {switch['hostname']}: VNI {vni_number} verified (state: {vni_state}, type: {vni_type})")

                # Check for missing expected VNIs
                missing_vnis = expected_vni_numbers - actual_vni_numbers
                issues.extend([
                    f"Expected VNI {vni} ({expected_vni_map[vni]['type_prefix']} {expected_vni_map[vni]['name']}) not found on switch"
                    for vni in missing_vnis if vni in expected_vni_map
                ])

                # Results
                if issues:
                    logger.error(f"{switch['hostname']} VNI verification failed:")
                    for issue in issues:
                        logger.error(f"  - {issue}")
                    step.failed(f"{len(issues)} VNI issue(s) found on {switch['hostname']}")
                else:
                    logger.info(f"{switch['hostname']}: All {len(actual_vnis)} VNIs verified successfully")
                    step.passed(f"All VNIs on {switch['hostname']} verified successfully")
