import io
import time
import threading
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
# from sklearn.cluster import KMeans
from matplotlib.colors import rgb_to_hsv
from skimage.feature import hog
from sklearn.externals import joblib
import requests

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = [] 

API_AI = "192.168.1.113"
API_DETECT_OBJECT="http://192.168.1.113:8082/trash/detect-object"

port = 9000
message =None
trash = None 


#####

def uploadImage(url, params, file):
    """
    uploads an image given the upload url [string], extra parameters [string], and file [bytes]
    """
    # parameters for image upload
    post_params = {'parameters': params}
    # convert the BytesIO file object to a viable file parameter
    files = {'file': file}
    # POST request with the parameters for upload
    r = requests.post(url, data=post_params, files=files)
    return r

def crop_img(img):
    cropx = 300
    cropy = 300
    y, x, _ = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty + cropy, startx:startx + cropx]

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def crop_img_2(img):
    cropx = 480
    cropy = 480
    y, x, _ = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    img = img[starty:starty + cropy, startx:startx + cropx]
    return img
 


class TrashControlServerTask(threading.Thread):
    def __init__(self):
        """ClientTask"""
        threading.Thread.__init__ (self)
    
    def run(self):
        global message
        context = zmq.Context()
        socket = context.socket(zmq.REP) 
        socket.bind("ipc:///tmp/sensor:9999") 
        #OpenCamera Here... 
        while True:
            try:
                data = socket.recv_json()
                time.sleep(1)
                socket.send("1")
                print("{0}".format(data)) 
                #Neu la Open => wait  3 second -> to take picture.
                time.sleep(2)
                message=data 

            except Exception as e:
                print e.message()
                
 
class TrashControlClientTask():
    """ClientTask"""
    def __init__(self): 
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('ipc:///tmp/actuator:9999')

    def send(self, message):
        print "send :%s " % message  
        self.socket.send_json(message)
        data = self.socket.recv_json()
        print data
        return data

    def send_led(self, colorValue):
        #Supported Colors: red, green, blue, white, none
        message = {
            "Instruction" : "WRITE",
            "ID": "SET_LED_COLOR",
            "Color": colorValue
            }
        return self.send(message) 


    def send_go_home(self):
        message={
                "Instruction" : "WRITE",
                "ID": "GO_HOME"   
                }
        self.send(message)
        #data = self.socket.recv_json()
        #print data 

    def send_close_cover_case(self):
        message={
                "Instruction" : "WRITE",
                "ID": "CLOSE_COVER"   
                } 
        self.send(message)
        #data = self.socket.recv_json()
        #print data 

    def send_go_trash(self):

        self.send_led("white")

        message={
            "Instruction" : "WRITE",
            "ID": "GO_TRASH"   
            }
        self.send(message)
        #data = self.socket.recv_json()
        #print data 
        #self.send_go_home()
        #data = self.socket.recv_json()
        #print data 
        self.send_led("blue")

    
    def send_go_recycle(self):
        
        self.send_led("green")
        
        message={
                "Instruction" : "WRITE",
                "ID": "GO_RECYCLE"   
                }
        #time.sleep(5000)
        self.send(message) 
        #self.send_go_home()
        self.send_led("blue")

    def close(self):
        self.socket.close()
        self.context.term()


class WifiManager(threading.Thread):
    def __init__(self):
        self.terminated=False
    
    def run(self):
        pass

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
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
            
    def run(self):
        # This method runs in a separate thread
        global done
        global message  
        
        t = time.time()
        channel = implementations.insecure_channel(API_AI, int(port))
        stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
        print(time.time() - t)
        detect_count = 0

        while not self.terminated:
            # Wait for an image to be written to the stream
            print "Wait for an image to be written to the stream"
            if self.event.wait(1):
                try:
                    ###Get New Frame here....
                    print "get_images" 
                    self.stream.seek(0)  
                    pil = Image.open(self.stream)
                    if detect_count > 0 :
                        detect_count=detect_count+1
                        print "Sleep %d " % detect_count 
                        time.sleep(1)

                    if message!=None and message["ID"]=="SCAN_WIFI_SSID":
                        message = None  
                        # create a reader
                        scanner = zbar.ImageScanner() 
                        # configure the reader
                        scanner.parse_config('enable') 
                        pil = pil.convert('L')
                        pil = crop_img(pil) # Add
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
                            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                            datajson = symbol.data 
                            try: 
                                wifi_extract=json.loads(datajson)
                                #Call ConnectWifi.

                            except Exception as e:
                                raise ParseError(e)

                    ####                            
                    if (detect_count==0 or detect_count >=10) and message!=None and message["ID"]=="COVER_STATUS" and message["Value"]==1: 
                         
                        print "start_detect_backgroud" 
                        file_name="/home/pi/trashimages/%d/%d_%d_%f.jpg" % (3, int(time.time()) , 0 , 0 )
                        print file_name
                        pil.save(file_name, format='JPEG') 
                        # has_obj = 0
                        # send image to server.
                        output = io.BytesIO()
                        output_2 = io.BytesIO() # add
                        pil.save('crop_image.jpg', format='JPEG')
                        pil = np.asarray(pil)
                        pil_2 = crop_img_2(pil) # add
                        pil = crop_img(pil)
                        pil = Image.fromarray(pil.astype('uint8'), 'RGB')
                        print(pil)
                        pil.save(output, format='JPEG')
                        pil_2 = Image.fromarray(pil_2.astype('uint8'), 'RGB') # add
                        pil_2.save(output_2, format='JPEG') # add
                        data = output.getvalue()
                        data_2 = output_2.getvalue()
                        re = uploadImage(API_DETECT_OBJECT, {}, data)
                        self.detect_object_count = re.json()['status']
                        print "Has Object : %d " % self.detect_object_count
                        print '#####'
                        # has_obj = requests.post("http:..../detect-object", files=files, data={})
                        # has_obj = detect_background(pil)
                        
                        if self.detect_object_count == 0:
                            trash.send_led("red")
                            print "get_images_again" 
                            if detect_count >=6 :
                                detect_count =0
                                message = None 
                                trash.send_close_cover_case()

                            else :            
                                detect_count=detect_count+1

                            time.sleep(1)

                        if self.detect_object_count == 1:
                            print "object"
                            detect_count = 0
                            message = None     
                            self.detect_object_count =0
                            trash.send_led("blue") 
                            trash.send_close_cover_case()
                            t = time.time()
                            request = predict_pb2.PredictRequest()
                            request.model_spec.name = "recycle"
                            request.model_spec.signature_name = "scores"
                            request.inputs["image"].CopyFrom(tensor_util.make_tensor_proto([data]))

                            print(time.time() - t) 
                            t = time.time()
                            result = stub.Predict(request, 10.0)

                            # add
                            request_2 = predict_pb2.PredictRequest()
                            request_2.model_spec.name = "recycle"
                            request_2.model_spec.signature_name = "scores"
                            request_2.inputs["image"].CopyFrom(tensor_util.make_tensor_proto([data_2]))
                            result_2 = stub.Predict(request_2, 10.0)
                            ###
                            prob = tensor_util.MakeNdarray(result.outputs["prob"])
                            prob_2 = tensor_util.MakeNdarray(result_2.outputs["prob"]) # add
                            # print prob[0]
                            # print prob_2[0] # add
                            if max(prob[0]) > max(prob_2[0]):
                                result = result
                            elif max(prob_2[0]) >= max(prob[0]):
                                print 'CHANGE'
                                result = result_2

                            class_id = tensor_util.MakeNdarray(result.outputs["class_id"]) 
                            result_value = self.mapping_class( class_id ) 
                            print "result object is: %d " % result_value  
                            index = np.argmax(prob[0])

                            ##prob[0][index] < 0.35 ->
                            time.sleep(1)
                            if result_value == 1 and prob[0][index] >=0.3:
                                #tai' che 
                                trash.send_go_recycle() 
                                print "1" 
                            elif result_value == 0 and prob[0][index] >=0.3:
                                #ko tai che.
                                print "0"
                                trash.send_go_trash() 
                            else:
                                # Khong phan biet duoc rac nao.
                                print "Khong phan biet duoc rac nao."
                                trash.send_led("red") 
                                #Lang nghe user dong Nap nao=>
                                #Lay ket qua phan loai.
                                #Store xuong local. 
                                result_value = 2
                                print result_value   
                            
                            file_name="/home/pi/trashimages/%d/%d_%d_%f.jpg" % (result_value, int(time.time()) , class_id[0] , prob[0][index] )
                            print file_name
                            pil.save(file_name, format='JPEG') 
                                
                            time.sleep(3) 
                        else: 
                            print "..."


                    #Bam go_trash
                    if message!=None and message["ID"]=="TRASH_BUTTON" and message["Value"]==2:
                        print "GoTRash"
                        message = None   
                        # Xu ly up_data_truoc do_len_cho server store images. 
                    if message!=None and message["ID"]=="RECYCLE_BUTTON" and message["Value"]==3:
                        print "Go RECYCLE_BUTTON"
                        message = None   
                        # Xu ly up_data_truoc do_len_cho server store images.
                    del pil
                    #trash.close()

                finally:
                    print "#Reset the stream and event"
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    #self.trash.close()
                    with lock:
                        pool.append(self)
 
def streams():
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
 
 


if __name__ == "__main__": 
    # t = time.time() 
    print "Start product listen events"
    serverTask = TrashControlServerTask()
    serverTask.start()    
    trash = TrashControlClientTask()
    trash.send_led("blue")

    ## Start Camera.
    with picamera.PiCamera() as camera:
        pool = [ImageProcessor()] # for i in range(4)]
        camera.resolution = (640, 480)
        camera.framerate = 20
        #camera.brightness = 60 
        time.sleep(2)
        camera.capture_sequence(streams(), use_video_port=True) 
    while pool:
            with lock:
                processor = pool.pop()
            processor.terminated = True
            processor.join()
         
#MAC_ADDRESS: b8:27:eb:40:43:a3




