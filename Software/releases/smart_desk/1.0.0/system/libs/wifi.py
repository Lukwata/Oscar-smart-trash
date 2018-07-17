#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
#phuong macbook
from aos.system.libs.util import Util

class WifiHostpot:
    _ssid = "Autonomous"

    # init
    def __init__(self, ssid=None):
        if ssid is not None:
            self._ssid = ssid# + "_" + Util.gen_id()

    def start_hotspot(self):
        print "Creating hostpot '" + self._ssid + "' ...."
        Util.cmd("sudo ap " + str(self._ssid), True)
        print "running..."

    def start_hotspot_with_custom_wpa(self, wpa):
        Util.cmd("sudo ap " + self._ssid + " " + wpa, False)
        print "running..."

    def stop_hotspot_and_connect_wifi(self, ssid, wpa):
        print "Stop hostpot and connecting wifi ssid: %s, wpa: %s ..." % (str(ssid), str(wpa))
        Util.cmd("sudo sta '%s' '%s'" % (str(ssid), str(wpa)), True)
        # sleep(10) # neu uncomment thi chinh False ham tren thanh True
        return Util.check_internet_connection()