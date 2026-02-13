import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from pyats import aetest
from pyats.topology import loader
from unicon.core.errors import ConnectionError
import logging
from nac_yaml.yaml import load_yaml_files
from aetest_bgw_rs_evpn_neighbor_test import VerifyBgwBgpL2vpnEvpnNeighbors
from aetest_nve_vnis_test import VerifyNveVnis


logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def load_data_model_files(self, data_model_dir):
        """Load data model files"""
        data = {}
        data.setdefault('data', {})
        data['data'] = load_yaml_files([data_model_dir])

        self.parent.parameters.update({'fabric': data['data']['vxlan']['fabric']['name']})
        self.parent.parameters.update(data)

    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        if len(testbed.devices) == 0:
            self.failed('{testbed} is empty'.format(testbed=str(testbed)))
        else:
            try:
                self.fabric = self.parent.parameters['fabric']
                logger.info(f"Connecting to {self.fabric}...")
                testbed.devices[self.fabric].connect(via='rest')
            except (TimeoutError, ConnectionError):
                logger.error(f"Unable to connect to {self.fabric}")

    @aetest.subsection
    def check_connection(self, testbed, steps):
        # Loop over every device in the testbed
        with steps.start(f"Test connection status for {testbed.devices[self.fabric]}", continue_=True) as step:
            if testbed.devices[self.fabric].connected:
                logger.info(f"{self.fabric} connected status: {testbed.devices[self.fabric].connected}")
            else:
                logger.error(f"{self.fabric} connected status: {testbed.devices[self.fabric].connected}")
                step.failed()

    @aetest.subsection
    def get_nd_inventory(self, testbed):
        # Parse into organized structure
        inventory = {}
        inventory.setdefault('inventory', {})
        inventory['inventory'].setdefault(self.fabric, {})

        api = f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{self.fabric}/inventory/switchesByFabric"
        logger.info(f"Querying fabric {self.fabric} inventory endpoint...")

        try:
            switches = testbed.devices[self.fabric].rest.get(api)

            for switch in switches:
                fabric_name = switch['fabricName']
                logical_name = switch['logicalName']

                # Create fabric entry if it doesn't exist
                if fabric_name not in inventory['inventory'][self.fabric] :
                    inventory['inventory'][self.fabric][fabric_name] = {}

                # Add switch under its fabric
                inventory['inventory'][self.fabric][fabric_name][logical_name] = {
                    'ip': switch['ipAddress'],
                    'id': switch['switchDbID'],
                    'role': switch['switchRole'].replace(' ', '_')
                }

        except Exception as exc:  # pylint: disable=broad-except
            logger.error(f"Failed to get inventory for fabric {self.fabric}: {exc}")
            self.failed(f"Failed to get inventory for fabric {self.fabric}")

        self.parent.parameters.update(inventory)


class VerifyBgwBgpL2vpnEvpnNeighbors(VerifyBgwBgpL2vpnEvpnNeighbors):
    logger.info(f"Executing BGW BGP L2VPN EVPN neighbors verification test case...")


class VerifyNveVnis(VerifyNveVnis):
    logger.info(f"Executing VNIs status verification test case...")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        if testbed.devices[self.parent.parameters['fabric']].connected:
            logger.info(f"Disconnecting from {self.parent.parameters['fabric']}...")
            testbed.devices[self.parent.parameters['fabric']].disconnect()


if __name__ == '__main__':
    aetest.main()
