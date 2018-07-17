from __future__ import print_function

import io
import time
import threading
import subprocess 
from subprocess import Popen, PIPE
from threading import Timer
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
import time 
def postData(url, params, file,token ):
    """
    uploads an image given the upload url [string], extra parameters [string], and file [bytes]
    """
    try:
        # parameters for image upload
        #post_params = {'parameters': params}
        # convert the BytesIO file object to a viable file parameter
        files = {'link': file} 
        # POST request with the parameters for upload
        #'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        headers = {
            'Authorization': 'JWT ' + token
        }
        t = time.time() 

        if(file == None ):
            r = requests.post(url, data=params, headers=headers)
        else:
            r = requests.post(url, data=params, headers=headers, files=files) 
        print(time.time() - t)  
        print (r.text)
        if r.status_code >=200 and r.status_code <=300 :
            return r.json()
        else:
            return None 
    except Exception as e:
        print (e.message)
        return None


def postData2(url,  file,token ):
    """
    uploads an image given the upload url [string], extra parameters [string], and file [bytes]
    """
    try:
        # parameters for image upload
        #post_params = {'parameters': params}
        # convert the BytesIO file object to a viable file parameter
        #files = {'link': file} 
        # POST request with the parameters for upload
        #'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        headers = {
            'Authorization': 'JWT ' + token
        }
        
        t = time.time() 
        
        r = requests.post(url, data=file, headers=headers) 

        print(time.time() - t)  
        print (r.text)
        if r.status_code >=200 and r.status_code <=300 :
            #return r.json()
            result = r.json()
            ai_result = {}
            ai_result["type_ai"]= int(result["result"])
            return ai_result
        else:
            return None 
    except Exception as e:
        print (e.message)
        return None


def postDataFile(url, params, file,token ):
    """
    uploads an image given the upload url [string], extra parameters [string], and file [bytes]
    """
    try:
        # parameters for image upload
        #post_params = {'parameters': params}
        # convert the BytesIO file object to a viable file parameter
        files = {'link': open(file,'rb')}  
        # POST request with the parameters for upload
        #'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        headers = {
            'Authorization': 'JWT ' + token
        }
        t = time.time() 

        r = requests.post(url, data=params, headers=headers, files=files) 
        
        print(time.time() - t)  

        if r.status_code >=200 and r.status_code <=300 :
            return r.json()
        else:
            return None 
    except Exception as e:
        print (e.message)
        return None

def post3DataFile(url, params, fontcam, leftcam,rightca ,token ):
    """
    uploads an image given the upload url [string], extra parameters [string], and file [bytes]
    """
    try:
        # parameters for image upload
        #post_params = {'parameters': params}
        # convert the BytesIO file object to a viable file parameter
        #files = {'link': fontcam, 'link2': open(leftcam,'rb'), 'link3': open(rightca,'rb')}  
         
        multiple_files = [   ('link', ('link', fontcam)),
                            ('link2', ('link2', open(leftcam, 'rb'), 'image/jpg')),
                            ('link1', ('link1', open(rightca, 'rb'), 'image/jpg'))]

        headers = {
            'Authorization': 'JWT ' + token
        }
        t = time.time() 

        r = requests.post(url, data=params, headers=headers, files=multiple_files) 
        
        print(time.time() - t)  

        if r.status_code >=200 and r.status_code <=300 :
            return r.json()
        else:
            return None 
    except Exception as e:
        print (e.message)
        return None


def execute_cmd_return(cmd, timeout_sec):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()

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


def read_file(file):
    data = None
    try:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
            except:
                return None

    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        print (file)

    return data


def write_file(file, message):
    try:
        with open(file, 'w+') as f:
            json.dump(message, f)
        # respone = {"status":"1", "message":"success"}
        # socket.send_json(respone)
        return True

    except IOError as e:
        print( "I/O error({0}): {1}".format(e.errno, e.strerror))
        print (file)
        return False 
    

def check_internet():
    try: 
        url = 'https://google.com'
        timeout = 10
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
        return False