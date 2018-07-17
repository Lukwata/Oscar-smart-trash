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

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = [] 

host = "192.168.1.113"
port = 9000
message =None

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
                



class TrashControlClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self): 
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('ipc:///tmp/actuator:9999')  

        #socket send...

        socket.close()
        context.term()


class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.wifi_status= False 
        self.start() 

    def run(self):
        # This method runs in a separate thread
        global done
        global message
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    ###Get New Frame here....
                    ###Processs any if you want.  
                    # print "process post image "
                    #print("In Images process : {0}".format(message))  

                    if message!=None and message["ID"]=="COVER_STATUS" and message["Value"]==1:
                        #done
                        message = None  
                        self.stream.seek(0)  
                        pil = Image.open(self.stream)
                        ######################################### 
                        # create a reader
                        scanner = zbar.ImageScanner() 
                        # configure the reader
                        scanner.parse_config('enable') 
                        pil = pil.convert('L')
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
                                print "ssid: %s" % wifi_extract["ssid"]
                            except Exception as e:
                                raise ParseError(e)
 
                            
                    # t = time.time()
                    # request = predict_pb2.PredictRequest()
                    # request.model_spec.name = "recycle"
                    # request.model_spec.signature_name = "scores"
                    # request.inputs["image"].CopyFrom(tensor_util.make_tensor_proto([data]))
                    # print(time.time() - t) 
                    # t = time.time()
                    # #send images to server.
                    # result = stub.Predict(request, 10.0)
                    # print(tensor_util.MakeNdarray(result.outputs["prob"])) 
                    # done = True  

                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
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
    # channel = implementations.insecure_channel(host, int(port))
    # stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    # print(time.time() - t)
    print "Start product listen events"
    serverTask = TrashControlServerTask()
    serverTask.start() 

    ## Start Camera.
    with picamera.PiCamera() as camera:
        pool = [ImageProcessor()] # for i in range(4)]
        camera.resolution = (640, 480)
        camera.framerate = 10 
        time.sleep(2)
        camera.capture_sequence(streams(), use_video_port=True) 
    while pool:
            with lock:
                processor = pool.pop()
            processor.terminated = True
            processor.join()
        






