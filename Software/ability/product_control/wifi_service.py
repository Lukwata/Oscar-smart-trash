from __future__ import print_function

import io
import time
import threading
import subprocess
import picamera
import json
from PIL import Image 
import zbar
import time 
import numpy as np
from grpc.beta import implementations
import zmq
from apis import (prediction_service_pb2, predict_pb2, dtypes, tensor_pb2,
                  tensor_util)

from sklearn.cluster import KMeans 
from matplotlib.colors import rgb_to_hsv 
from ProductControl import ProductControl
from Commands import COMMANDS
from help import Help
from aos.system.libs.util import Util
import requests
#from cron_update_ability import CronUpdateAbility
#from cron_check_internet import CronCheckInternet
#from check_update import CheckFirmwareUpdate
from aos.system.sdk.python.service_wrapper import AutonomousService
from trashControl import TrashControlClientTask 
import helpers

SETTING_FILE = "/home/pi/aos/data/product_settings.json"
 
ZMQ_WIFI_SERVICE_PORT="tcp://127.0.0.1:9950"

WIFI_STATUS = False

class WifiManager(object): 
    _context = None
    _socket =None

    def __init__(self):
        self._context = None

    def server(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(ZMQ_WIFI_SERVICE_PORT)  
        info_rev = None
        while True:
            #foreach...
            respone = {"status": 0, "message": "" }
            info_rev = self._socket.recv_json() 
            print (info_rev)
            check_info = True
            try: 
                if info_rev['ssid'] == "":
                    check_info = False
                if info_rev['pass'] == "":
                    check_info = False
                if check_info:
                    respone = {"status": 1, "message": ""}
                    self._socket.send_json(respone)
                    command = 'sudo /home/pi/aos/ability/product_control/wifi.sh '+ info_rev["ssid"] + ' ' + info_rev["pass"]
                    print(command)
                    percent = helpers.execute_cmd_return(command)  
                    time.sleep(5)
                    helpers.write_file(SETTING_FILE,info_rev)
                else:
                    self._socket.send_json(respone)
            except:
                self._socket.send_json(respone)
        self._socket.close()
        self._context.term()  
 

###======================================#### 
if __name__ == '__main__':
    # t = time.time() 
    print( "____init_____")   
    wifiManager  = WifiManager() 
    wifiManager.server() 