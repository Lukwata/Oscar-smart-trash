import unittest
import os
import time
import mock
from mock import patch

from aos.system.libs.wifi import WifiHostpot
from aos.system.libs.wifi import RasberryWifi

class WifiTestCase(unittest.TestCase):

    def setUp(self):
        self.wifi = WifiHostpot()
        self.rasberryWifi = RasberryWifi()

    def tearDown(self):
        pass
    
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_list_network")
    def test_rasbperry_list_networks(self, list_networks):
        list_networks.return_value = """
                                    Selected interface 'wlan0'
                                    network id / ssid / bssid / flags
                                    0	AutonomousTech	any	[CURRENT]
                                    1	AutonomousSale	any	[DISABLED]
                                    2	AutonomousSale	any	[DISABLED]
                                    3	AutonomousSale	any	[DISABLED]
                                    4	AutonomousTech	any	[DISABLED]
                                    5	AutonomousTech	any	[DISABLED]
                                    6	AutonomousSale	any	[DISABLED]
                                    7	AutonomousTech	any	[DISABLED]
                                    8	AutonomousTech	any	[DISABLED]
                                    """

        networks = self.rasberryWifi.network_list()
        self.assertEqual(networks[0]['name'], "AutonomousTech")
        self.assertEqual(networks[0]['id'], 0)
        self.assertTrue(networks[0]['active'])
        self.assertFalse(networks[1]['active'])

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_network")
    def test_add_network(self, cmd_add_network):
        cmd_add_network.return_value = """
                                        Selected interface 'wlan0'
                                        1
                                        """
        network_id = self.rasberryWifi._add_network()
        self.assertEqual(network_id, 1)

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_ssid")
    def test_add_ssid_success(self, cmd_add_ssid):
        cmd_add_ssid.return_value = """
                                        Selected interface 'wlan0'
                                        OK
                                        """
        actual = self.rasberryWifi._add_ssid(1, "AutonomousSale")
        self.assertTrue(actual)

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_ssid")
    def test_add_ssid_fail(self, cmd_add_ssid):
        cmd_add_ssid.return_value = """
                                        Selected interface 'wlan0'
                                        FAIL
                                        """
        actual = self.rasberryWifi._add_ssid(1, "AutonomousSale")
        self.assertFalse(actual)

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_psk")
    def test_add_psk(self, _cmd_add_psk):
        _cmd_add_psk.return_value = """
                                        [1] 14449
                                        Selected interface 'wlan0'
                                        Selected interface 'wlan0'
                                        OK
                                        OK
                                        [1]+  Done                    sudo wpa_cli set_network 1 psk '"autonomous123"'
                                        """
        actual = self.rasberryWifi._add_psk(1, "AutonomousSale")
        self.assertTrue(actual)

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_psk")
    def test_add_psk_fail(self, _cmd_add_psk):
        _cmd_add_psk.return_value = """
                                        [1] 14449
                                        Selected interface 'wlan0'
                                        Selected interface 'wlan0'
                                        OK
                                        FAIL
                                        [1]+  Done                    sudo wpa_cli set_network 1 psk '"autonomous123"'
                                        """
        actual = self.rasberryWifi._add_psk(1, "AutonomousSale")
        self.assertFalse(actual)

    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_list_network")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_network")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_ssid")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_add_psk")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_enable_network")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_select_network")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_save_config")
    @mock.patch("aos.system.libs.wifi.RasberryWifi._cmd_reconfigure_network")
    def test_connect_wifi_with_right_config(self, _cmd_reconfigure_network, _cmd_save_config, _cmd_select_network, _cmd_enable_network, _cmd_add_psk, cmd_add_ssid, _cmd_add_network, _cmd_list_network):
        _cmd_reconfigure_network.return_value = ""
        _cmd_save_config.return_value = ""
        _cmd_select_network.return_value = ""
        _cmd_enable_network.return_value = ""
        _cmd_list_network.return_value = """
                                    Selected interface 'wlan0'
                                    network id / ssid / bssid / flags
                                    0	AutonomousTech	any	[DISABLED]
                                    1	AutonomousSale	any	[DISABLED]
                                    2	AutonomousSale	any	[DISABLED]
                                    3	AutonomousSale	any	[DISABLED]
                                    4	AutonomousTech	any	[DISABLED]
                                    5	AutonomousTech	any	[DISABLED]
                                    6	AutonomousSale	any	[DISABLED]
                                    7	AutonomousTech	any	[DISABLED]
                                    8	AutonomousTech	any	[CURRENT]
                                    """
        _cmd_add_network.return_value = """
                                    Selected interface 'wlan0'
                                    1
                                    """

        cmd_add_ssid.return_value = """
                                    Selected interface 'wlan0'
                                    OK
                                    """

        _cmd_add_psk.return_value = """
                                    [1] 14449
                                    Selected interface 'wlan0'
                                    Selected interface 'wlan0'
                                    OK
                                    OK
                                    [1]+  Done                    sudo wpa_cli set_network 1 psk '"autonomous123"'
                                    """

        actual = self.rasberryWifi.connect_wifi("AutonomousTech", "autonomous123")
        self.assertTrue(actual)

        actual = self.rasberryWifi.connect_wifi("'pikachu'", wpa='')
        self.assertTrue(actual)

if __name__ == '__main__':
    unittest.main()
