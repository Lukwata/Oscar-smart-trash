#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
#phuong macbook
import time

from aos.system.libs.util import Util

class WifiHostpot:
    _ssid = "Autonomous"

    # init
    def __init__(self, ssid=None):
        if ssid is not None:
            self._ssid = ssid + "-" + Util.gen_id()

    def start_hotspot(self):
        print "Creating hostpot '" + self._ssid + "' ...."
        Util.cmd("sudo ap " + str(self._ssid), True)
        print "running..."

    def start_hotspot_with_custom_wpa(self, wpa):
        Util.cmd("sudo ap " + self._ssid + " " + wpa, False)
        print "running..."

    def stop_hotspot_and_connect_wifi(self, ssid, wpa):
        print "Stop hostpot and connecting wifi ssid: %s, wpa: %s ..." % (ssid.encode("UTF-8"), wpa.encode("UTF8"))
        wifi = RasberryWifi()
        if wpa is not None and len(wpa) != 0:
            wifi.connect_wifi(ssid=ssid.encode("UTF8"), wpa=wpa.encode("UTF8"))
        else:
            wifi.connect_wifi(ssid=ssid.encode("UTF8"), wpa='')
        return Util.check_internet_connection()

class RasberryWifi(object):
    
    def __init__(self, iface='wlan0'):
        self.iface = iface

    def connect_wifi(self, ssid, wpa):
        networks = self.network_list()
        network_id = self._is_ssid_in_network_list(ssid, networks)
        if network_id == -1:
            network_id = self._add_network()
            if network_id == -1:
                return False
            elif self._add_ssid(network_id, ssid) == False:
                return False

        if self._add_psk(network_id, wpa):    
            self._cmd_enable_network(network_id)
            self._cmd_select_network(network_id)
            self._cmd_save_config()
            self._cmd_reconfigure_network()
            time.sleep(12)
        else:
            return False
        return True

    def network_list(self):
        networks = []
        response = self._cmd_list_network()
        for line in response.splitlines():
            items = line.strip("\n").split("\t")
            if len(items) == 4:
                try:
                    network_id = int(items[0])
                    network_name = items[1].decode("string-escape")
                    active = False
                    if items[3] == "[CURRENT]": 
                        active = True
                    item = {"id": network_id, "name": network_name, "active": active} 
                    networks.append(item)
                except Exception as ex:
                    print(str(ex))
                
        return networks

    def active_network(self):
        networks = self.network_list()
        for network in networks:
            if network['active']:
                return network['name'].decode("string-escape")
        return ""

    def _add_network(self):
        response = self._cmd_add_network()
        network_id = -1
        for line in response.splitlines():
            items = line.strip().split(" ")
            if len(items) == 1:
                try:
                    network_id = int(items[0])
                    return network_id
                except Exception as ex:
                    next

        return network_id

    def _add_ssid(self, network_id, ssid):
        response = self._cmd_add_ssid(network_id, ssid)
        result = self._parse_result(response)
        return result

    def _add_psk(self, network_id, psk):
        response = self._cmd_add_psk(network_id, psk)
        if psk is None or len(psk) == 0:
            return self._parse_result(response)
        
        checking_required = 1
        if psk is not None and len(psk) != 0:
            checking_required = 2
        for line in response.splitlines():
            items = line.strip().split(" ")
            if len(items) == 1:
                if len(items[0]) != 0:
                    if Util.smart_bool(items[0]):
                        checking_required = checking_required - 1

        if checking_required == 0:
            return True
        return False

    def _parse_result(self, response):
        result = False
        for line in response.splitlines():
            items = line.strip().split(" ")
            if len(items) == 1:
                if len(items[0]) != 0:
                    return Util.smart_bool(items[0])
        return result

    def _is_ssid_in_network_list(self, ssid='', networks=[]):
        for network in networks:
            if network['name'] == ssid:
                return network['id']
        return -1

    def _cmd_list_network(self):
        return Util.cmd("sudo wpa_cli list_networks")

    def _cmd_add_network(self):
        return Util.cmd("sudo wpa_cli add_network")

    def _cmd_reconfigure_network(self):
        return Util.cmd("sudo wpa_cli reconfigure")

    def _cmd_add_ssid(self, network_id, ssid):
        return Util.cmd("sudo wpa_cli set_network {} ssid {}".format(network_id, Util.toHex(ssid)))

    def _cmd_add_psk(self, network_id, psk=None):
        if psk is None or len(psk) == 0:
            return Util.cmd("sudo wpa_cli set_network {} key_mgmt NONE".format(network_id))
        else:
            return Util.cmd("sudo wpa_cli set_network {} psk '\"{}\"' & sudo wpa_cli set_network {} key_mgmt WPA-PSK ".format(network_id, psk, network_id))
    
    def _cmd_enable_network(self, network_id):
        try:
            _id = int(network_id)
            return Util.cmd("sudo wpa_cli enable_network {}".format(_id))
        except Exception as ex:
            pass

    def _cmd_select_network(self, network_id):
        return Util.cmd("sudo wpa_cli select_network {}".format(network_id))

    def _cmd_save_config(self):
        return Util.cmd("sudo wpa_cli save_config")
    