#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

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
from aos.system.sdk.python.service_wrapper import AutonomousService

from trashControl import TrashControlClientTask 
import helpers

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []  

host = "35.198.234.42"
API_AI = "35.198.234.42"
API_POST_IMG="http://35.198.228.87/api/image/"
API_POST_VERIFY = "http://35.198.228.87/api/image-profile/"
API_POST_ADD_PRODUCT = "http://35.198.228.87/api/product/"
API_POST_DELETE_PRODUCT = "http://35.198.228.87/api/product/" 



port = 9001
message =None
trash = None 
check_internet_connection = False
wifi_info = {}
init_state=0
TIME_CHECK = 10
MAX_COUNT = 3
MAX_TIME_DELAY = 6
ZMQ_WIFI_SERVICE_PORT="tcp://127.0.0.1:9950" 
SETTING_FILE = "/home/pi/aos/data/product_settings.json" 
IMAGE_TEST  ="image.jpg" 
PRODUCT_ID = ""  
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9zY2FyQGF1dG9ub21vdXMuYWkiLCJleHAiOjE1MzAzNDkwMTgsImlkIjo3OTc1Nn0.3SG7UnPHSfFLSSwb5gwL2sQJq-ThEO8LvSXSOVSKWcs"
 
class TrashControlServerTask(threading.Thread):
    def __init__(self):
        """ClientTask"""
        threading.Thread.__init__ (self)

    def run(self):
        global message, wifi_info , PRODUCT_ID, TOKEN
        context = zmq.Context()
        socket = context.socket(zmq.REP) 
        socket.bind("ipc:///tmp/sensor:9999") 
        #OpenCamera Here... 
        while True:
            try:
                data = socket.recv_json()
                time.sleep(1)
                socket.send("1")
                print("recive: {0}".format(data))  
                print("message: {0}".format(message)) 
                
                if data["ID"]=="RESET_BUTTON":
                    print ("RESET_BUTTON")

                    #call delete product ...
                    url = API_POST_DELETE_PRODUCT + str(PRODUCT_ID) + "/"
                    headers = {
                        'Authorization': 'JWT ' + TOKEN
                    }
                    try:
                        response = requests.delete(url, data=None, headers=headers) 
                        print (response) 
                    except:
                        print("error") 

                    trash.enable_local_control() 
                    message={}
                    message["ID"]="SCAN_WIFI_SSID"
                    trash.send_led("red") 
                    trash.send_open_cover_case()  
                    cmd =["rm","-rf", SETTING_FILE]
                    wifi_info = None 
                    helpers.execute_cmd_return(cmd, 5)  
                    trash.send_blink_led("red","MS_300") 

            except:
                print("error")

 
if __name__ == '__main__':
    # t = time.time() 
    global message
    print( "____init_____") 
    serverTask = TrashControlServerTask()
    serverTask.start()    