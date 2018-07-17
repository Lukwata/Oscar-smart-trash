#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

from __future__ import print_function
import os
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
DONE_CAM0 = False
DONE_CAM1 = False


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
                if message == None or (message["ID"]!="SCAN_WIFI_SSID" and message["ID"]!="WIFI_ERROR"):
                    if data["ID"]=="COVER_STATUS" and data["Value"]==1:
                        #trash.disable_local_control() 
                        #time.sleep(2)
                        trash.enable_local_control() 
                        message=data
                    if data["ID"]!="COVER_STATUS":
                        message=data

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
 


def capturecc(cam, timestrCam):
    global DONE_CAM0, DONE_CAM1
    if cam == "0":
        DONE_CAM0=False
    if cam == "1":
        DONE_CAM1=False
    
    print("start capturecc " + cam)
    os.sys
    t = time.time()
    #os.system("sudo fswebcam -d /dev/video"+cam+" -r 640x320 image"+cam+".jpg")

    if cam == "0":
        timestrCam = timestrCam + "_C1"
    if cam == "1":
        timestrCam = timestrCam + "_C2"

    os.system("sudo fswebcam -d /dev/video"+cam+" -r 640x320 --no-banner /home/pi/aos/data/saveIMG/"+timestrCam+".jpg")
    #print( time.time()-t)
    #print ("done")
    if cam == "0":
        DONE_CAM0=True
    if cam == "1":
        DONE_CAM1=True

class ImageProcessor(threading.Thread):

    channel = None#implementations.insecure_channel(API_AI, int(port))
    stub = None #prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = None 
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.imagebk = None 
        self.terminated = False
        self.wifi_status= False 
        self.detect_object_count=0 
        self.start() 

    def mapping_class(self, class_id):
        class_id = class_id[0]
        if class_id == 1 or class_id == 3 or class_id == 5 or class_id == 9 or class_id == 11 or class_id == 12:
            return 0
        elif class_id == 0 or class_id == 2 or class_id == 4 or class_id == 6 or class_id == 7 or class_id == 8 or class_id == 10:
            return 1
    
    def init_ai_streaming(self):
        print ("init streaming ai")
        try:
            self.channel = implementations.insecure_channel(API_AI, int(port))
            self.stub = prediction_service_pb2.beta_create_PredictionService_stub(self.channel)
            self.request = predict_pb2.PredictRequest()
            self.request.model_spec.name = "recycle"
            self.request.model_spec.signature_name = "scores"
        except:
            print ("fail streaming ai") 

    def post_request_ai(self,data): 
        try: 
            t = time.time() 
            self.request.inputs["image"].CopyFrom(tensor_util.make_tensor_proto([data])) 
            result = self.stub.Predict(self.request, 30.0)   
            print("Print TIME POST:")
            print(time.time() - t)  
            prob = tensor_util.MakeNdarray(result.outputs["prob"]) 
            print (prob[0])  
            class_id = tensor_util.MakeNdarray(result.outputs["class_id"]) 
            result_value = self.mapping_class( class_id )  
            index = np.argmax(prob[0])
            return {"result_value":result_value, "index":index, "prob": prob, "class_id": class_id}
        except Exception as e:
            print ("error",  e)
            self.init_ai_streaming() 
            return  {"result_value":3, "index":0, "prob": None,"class_id":None}
        
    def run(self):
        # This method runs in a separate thread
        global done
        global message  
        global wifi_info ,  PRODUCT_ID, TOKEN
        detect_count = 0
        #self.init_ai_streaming()

        while not self.terminated:
            # Wait for an image to be written to the stream 
            if self.event.wait(1):
                try:
                    ###Get New Frame here....
                    print ("get_images") 
                    self.stream.seek(0)  
                    pil = Image.open(self.stream)
                    

                    if detect_count > 0 :
                        detect_count=detect_count+1
                        print ("Sleep %d " % detect_count)
                        time.sleep(1)
                        if detect_count >= (MAX_TIME_DELAY + MAX_TIME_DELAY):
                            detect_count =0
                            message = None  
                    if message!=None and message["ID"]=="SCAN_WIFI_SSID":
                        
                        outputstream = io.BytesIO() 
                        pil.save(outputstream, format='JPEG')  
                        data_image_post_reconnect = outputstream.getvalue()  

                        print ("...Waiting for QR_CODE setup...")
                        #message = None  
                        # create a reader
                        scanner = zbar.ImageScanner() 
                        # configure the reader
                        scanner.parse_config('enable') 
                        pil = pil.convert('L')
                        #pil = crop_img(pil) # Add
                        width, height = pil.size
                        raw = pil.tobytes() 
                        # wrap image data
                        image = zbar.Image(width, height, 'Y800', raw) 
                        # scan the image for barcodes
                        scanner.scan(image) 
                        # extract results
                        datajson= None 
                        for symbol in image:
                            # do something useful with results
                            print ('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)
                            datajson = symbol.data 
                            try: 
                                wifi_info=json.loads(datajson) 
                                try:
                                    message["ID"] = "WIFI_PROCESSING" 
                                    trash.send_blink_led("red","MS_50")
                                    command = ['sudo','/home/pi/aos/ability/product_control/wifi.sh',wifi_info["ssid"], wifi_info["pass"]]
                                    print(command)
                                    percent = helpers.execute_cmd_return(command,10)   
                                    message= None
                                    wifi_connect_check= False
                                    counntt = 0 
                                    while counntt <=5:
                                        if (helpers.check_internet()==True):
                                            message = None 
                                            print ("reconnect---")
                                            if wifi_connect_check == False:
                                                wifi_connect_check = True
                                                trash.send_turn_off_blink_led()
                                                trash.send_led("blue")
                                                trash.send_close_cover_case()
                                            #Add PRODUCT_ID    
                                            try:
                                                addresult = helpers.postData(API_POST_ADD_PRODUCT,{"name":"Oscar"}, None , wifi_info["token"] )
                                                print(addresult)
                                                if addresult != None :
                                                    PRODUCT_ID = addresult["id"]
                                                    wifi_info["product_id"]=PRODUCT_ID
                                                    #TOKEN = wifi_info["token"]
                                                    helpers.write_file(SETTING_FILE,wifi_info)

                                                    counntt = 10
                                                    break;
                                                else :
                                                    addresult = None  
                                            except Exception as ex:
                                                print (str(ex) ) 
                                                addresult = None

                                        time.sleep(1)
                                        counntt = counntt+1

                                    if wifi_connect_check ==False:
                                        message= None
                                        trash.send_blink_led("red","MS_300")
                                        message={}
                                        message["ID"]="SCAN_WIFI_SSID"

                                except Exception as ex:
                                    print (str(ex) )
                                
                            except Exception as e:
                                raise ParseError(e)

                    ####                            
                    if (detect_count==0 or detect_count >=MAX_TIME_DELAY) and message!=None and message["ID"]=="COVER_STATUS" and message["Value"]==1:
                        
                        timestr = time.strftime("%d%m%Y-%H%M%S")
                        t1 = threading.Thread(target=capturecc, args=("1",timestr,)).start()
                        t2 = threading.Thread(target=capturecc, args=("0",timestr,)).start()
                        timestr = "/home/pi/aos/data/saveIMG/"+ timestr + "_C0" + ".jpg"
                        pil.save(timestr, format='JPEG')
                        
                        output = io.BytesIO() 
                        #pil.save(output, format='JPEG')
                        data = output.getvalue()  
                        self.detect_object_count = 1 
                        print ("capture from front camera")
                        detect_count = 0
                        message = None     
                        self.detect_object_count =0 
                        trash.send_close_cover_case() 


                        # ai_result = helpers.post3DataFile(API_POST_IMG,{"category":1, "product":PRODUCT_ID}, 
                        # data, "/home/pi/aos/data/image0.jpg" , "/home/pi/aos/data/image1.jpg" , TOKEN )
                        # print (ai_result)
                        
                        #ai_result = helpers.postData(API_POST_IMG,{"category":1, "product":PRODUCT_ID}, data , TOKEN )
                        
                        #ai_result = helpers.postData2("http://192.168.1.113:8545/api/capture0", data , TOKEN )
#                        print("respone data from server imagemid")
#                        print(ai_result)
#                        if ai_result == None :
#                            ai_result = {"type_ai":0}
#                        #ai_result["type_ai"] = 2
#
#                        if ai_result["type_ai"] == 1: # and prob[0][index] >=0.3:
#                            #tai' che
#                            trash.send_go_recycle()
#                            print ("1" )
#                        elif ai_result["type_ai"]  == 0: # and prob[0][index] >=0.3:
#                            #ko tai che.
#                            print ("0")
#                            trash.send_go_trash()
#                        else:
#                            # Khong phan biet duoc rac nao.
#                            print ("Khong phan biet duoc rac nao.")
#                            trash.send_led("red")
#                            if 'id' in  ai_result:
#                                self.imagebk = ai_result["id"]
#                                ai_result["type_ai"] = 2
                        trash.send_led("blue")
                        #trash.enable_local_control() 
                        # if ai_result["type_ai"] == 2 and  'id' in  ai_result :
                        #     trash.disable_sensor_control()
                        
                    #Bam go_trash
                    if message!=None and message["ID"]=="TRASH_BUTTON" and message["Value"]==2:
                        print ("user press button Trash")
                        trash.enable_sensor_control()
                        message = None 
                        if self.imagebk !=None : 
                            ai_result = helpers.postData(API_POST_VERIFY,{"image":self.imagebk, "type":0 }, None , TOKEN )
                            print(ai_result)
                            self.imagebk = None 

                    if message!=None and message["ID"]=="RECYCLE_BUTTON" and message["Value"]==3:
                        print ("user press button RECYCLE_BUTTON")
                        trash.enable_sensor_control()
                        message = None 
                        if self.imagebk !=None :
                            ai_result = helpers.postData(API_POST_VERIFY,{"image":self.imagebk, "type":0 }, None , TOKEN )
                            print(ai_result)
                            self.imagebk = None  
                    del pil 
                finally: 
                    print ("finally stream")
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear() 
                    with lock:
                        pool.append(self)
 

class CameraServerTask(threading.Thread):
    def __init__(self):
        print ("""CameraServerTask""")
        threading.Thread.__init__ (self)

    def streams(self):
        global pool
        global lock 
        while not done:
            with lock:
                if pool:
                    processor = pool.pop()
                else:
                    processor = None
            if processor:
                yield processor.stream
                processor.event.set()
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)

    def run(self):
            ## Start Camera.
        global pool
        global lock 
        with picamera.PiCamera() as camera:
            pool = [ImageProcessor()] # for i in range(4)]
            camera.resolution = (640, 480)
            camera.framerate = 10
            #camera.brightness = 60 
            time.sleep(2)
            camera.capture_sequence(self.streams(), use_video_port=True) 
        
        print ("run camera Service")
        while pool:
                with lock:
                    processor = pool.pop()
                processor.terminated = True
                processor.join()  


        


def main(json_data, error):
     
    if error:
        return print (error)
    data = json_data['data']
    sensor = json_data['type'] if 'type' in json_data else None
    print( json_data) 
    # global check_internet_connection
    # global message
    # if sensor == COMMANDS.CHECK_INTERNET_CONNECTION:  
    #     print ("CHECK_INTERNET_CONNECTION")
    #     message={} 
    #     message["ID"] = "SCAN_WIFI_SSID"
    #     #cron_check_internet.reset()
    #     #cron_check_internet.run()  
    # else: 
    #     print (json_data) 
 
if __name__ == '__main__':
    # t = time.time() 
    global message
    print( "____init_____") 
    serverTask = TrashControlServerTask()
    serverTask.start()    

    trash = TrashControlClientTask()
    trash.send_led("red")

    # global init_state, wifi_info, PRODUCT_ID, TOKEN
    # init_state=0   

    CameraServer = CameraServerTask() 
    CameraServer.start() 
    wifi_info = helpers.read_file(SETTING_FILE)  

    print ("WIFI FILE INFO")
    print (wifi_info)
    if wifi_info == None : 
        message={}
        message["ID"] = "SCAN_WIFI_SSID"
        trash.send_blink_led("red","MS_300")
        trash.send_open_cover_case()  
    else: 
        PRODUCT_ID =  wifi_info["product_id"]
        #TOKEN = wifi_info["token"]

        if helpers.check_internet()==True:
            trash.send_led("blue") 
    print( "Main _ service ")
    AutonomousService().run(main)
    
