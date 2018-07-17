import io
import time
import threading
import picamera
import json
from PIL import Image
import numpy
import zbar
import time 
import numpy as np
import zmq

class TrashControlClientTask():
    """ClientTask"""
    def __init__(self): 
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('ipc:///tmp/actuator:9999')

    def send(self, message):
        print "send :"
        print message  
        self.socket.send_json(message)
        print self.socket.recv_json()
        

    def send_go_home(self):
        message={
                "Instruction" : "WRITE",
                "ID": "GO_HOME"   
                }
        self.send(message)

    def send_close_cover_case(self):
        message={
                "Instruction" : "WRITE",
                "ID": "CLOSE_COVER"   
                } 
        self.send(message)

    def send_go_trash(self):
        message={
            "Instruction" : "WRITE",
            "ID": "GO_TRASH"   
            }
        self.send(message)
    
    def send_go_recycle(self):
        message={
                "Instruction" : "WRITE",
                "ID": "GO_RECYCLE"   
                }
        self.send(message)

    def close(self):
        self.socket.close()
        self.context.term()

# a = TrashControlClientTask()
# a.send_go_home()
