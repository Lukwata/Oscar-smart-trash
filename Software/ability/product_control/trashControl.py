
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

      
class TrashControlClientTask():
    """ClientTask"""
    def __init__(self): 
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('ipc:///tmp/actuator:9999')

    def reconnect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('ipc:///tmp/actuator:9999')

    def send(self, message):
        print ("send :%s " % message) 
        try: 
            self.socket.send_json(message)
            data = self.socket.recv_json()
            print(data)
            return data
        except :
            print ("error _ zmq send message")
            self.reconnect() 
            self.socket.send_json(message)
            data = self.socket.recv_json()
            print(data)
            return data

       

    def send_led(self, colorValue):
        #Supported Colors: red, green, blue, white, none
        message = {
            "Instruction" : "WRITE",
            "ID": "SET_LED_COLOR",
            "Color": colorValue
            }
        return self.send(message) 

    ##========== Blink LED===============
    def send_blink_led(self, colorValue, timeloop):
        #Supported Colors: red, green, blue, white, none
        message = {
            "Instruction" : "WRITE",
            "ID": "SET_LED_COLOR",
            "Color": colorValue
            }
        self.send(message) 

        message = {
                    "Instruction" : "WRITE",
                    "ID": "SET_LED_BLINK",
                    "Value" :
                    {
                        "OnTime" :timeloop,
                        "OffTime": timeloop

                    }
                }
        self.send(message) 

    def send_turn_off_blink_led(self):
        message = {
                    "Instruction" : "WRITE",
                    "ID": "SET_LED_BLINK",
                    "Value" :
                    {
                        "OnTime" :"MS_0",
                        "OffTime": "MS_0"

                    }
                }
        self.send(message) 

    def send_go_home(self):
        message={
                "Instruction" : "WRITE",
                "ID": "GO_HOME"   
                }
        self.send(message)
        #data = self.socket.recv_json()
        #print data 

    def send_open_cover_case(self):
        message={
                "Instruction" : "WRITE",
                "ID": "OPEN_COVER"   
                } 
        self.send(message)
        
    def send_close_cover_case(self):
        message={
                "Instruction" : "WRITE",
                "ID": "CLOSE_COVER"   
                } 
        self.send(message)
        #data = self.socket.recv_json()
        #print data 

    def send_go_trash(self):

        #self.send_led("white") 
        self.send_blink_led("white","MS_300")
        message={
            "Instruction" : "WRITE",
            "ID": "GO_TRASH"   
            }
        self.send(message) 
        #self.send_led("blue")
        self.send_turn_off_blink_led()
        self.send_led("blue")

    
    def send_go_recycle(self):
        
        #self.send_led("green")
        self.send_blink_led("green","MS_300")
        message={
                "Instruction" : "WRITE",
                "ID": "GO_RECYCLE"   
                }
        #time.sleep(5000)
        self.send(message) 
        self.send_turn_off_blink_led()
        self.send_led("blue")

    def enable_local_control(self):
        message={
            "Instruction" : "WRITE",
            "ID": "LOCAL_CONTROL",
            "Value": "enable"
            } 
        self.send(message)  

    def disable_local_control(self):
        message={
            "Instruction" : "WRITE",
            "ID": "LOCAL_CONTROL",
            "Value": "disable"
            } 
        self.send(message)  
    
    def enable_sensor_control(self):
        message={
            "Instruction" : "WRITE",
            "ID": "SENSOR_CONTROL",
            "Value": "enable"
            } 
        self.send(message)  

    def disable_sensor_control(self):
        message={
            "Instruction" : "WRITE",
            "ID": "SENSOR_CONTROL",
            "Value": "disable"
            } 
        self.send(message)

    def close(self):
        self.socket.close()
        self.context.term()

 