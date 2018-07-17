from channel_util import local
import os

#default *-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-*-*
DEVICE_TYPE = os.environ['DEVICE_TYPE']
HOME_PATH = os.environ['HOME']
#*-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-**-*-*

#default:
LOCAL_HOTSPOT = "tcp://*:5004"

CURRENT_PATH = HOME_PATH + "/aos/"
BASE_APP = CURRENT_PATH + "ability/"
FIRMWARE_UPDATE__TMP_PATH = CURRENT_PATH + "tmp/"
REQUIREMENT_FIRMWARE_PATH = FIRMWARE_UPDATE__TMP_PATH + "system/requirements.txt"
BRAIN_CONFIG_PATH = CURRENT_PATH + "data/pr_device.json"
BRAIN_GO_CMD = "cd " + CURRENT_PATH + " && ulimit -s 1024 && ulimit -r 0 && chmod +x system/" + DEVICE_TYPE + "/brain && ./system/" + DEVICE_TYPE + "/brain -b " + BRAIN_CONFIG_PATH

BRAIN_TMUX_CMD = "unset TMUX && tmux new -s brain -n brain -d && tmux send-keys -t brain:brain '%s' C-m" % (BRAIN_GO_CMD)
KILL_BRAIN_TMUX_CMD = "tmux kill-session -t brain"

PATH_WIFI_CONFIG = CURRENT_PATH + 'data/os_config.json'
PATH_PRODUCT_ID_CONFIG = CURRENT_PATH + 'data/product_id.json'
PATH_USER_CONFIG = CURRENT_PATH + 'data/user.json'

# vision channels
FACIAL_RECOGNITION = local("facial_recognition")

IP_HOST_SPOT = '192.168.42.1'

__EMAIL_FIX__= '@autonomous.ai'

__FIREBASE_CONFIG__ = {
    "apiKey": "AIzaSyBBasZmVmXfTAXq0RfJFvU3ihJPxF9jE_k",
    "authDomain": "",
    "databaseURL": "https://personalrobot-1470372118376.firebaseio.com",
    "storageBucket": "",
    "serviceAccount": ""
  }
