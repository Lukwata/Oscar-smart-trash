
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

# Create a pool of image processors
done = False
#lock = threading.Lock()
pool = []  
host = "35.230.53.107"
API_AI = "35.230.53.107"
API_DETECT_OBJECT="http://192.168.1.113:8082/trash/detect-object"
API_CLOECT_DATA="http://192.168.1.113:8082/trash/detect-object" 
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


def sendWifiInfo(wifi):
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(config.ZMQ_WIFI_SERVICE_PORT)  
        print("WIFIClient sent %s" % wifi)
        socket.send_json(wifi)
        data = socket.recv_json() 
        socket.close()
        context.term()
        return data
    except:
        print ("cant connect to ZMQ")
        return None

sendWifiInfo({"ssid":"Autonomous","pass":"Autonomous"})
