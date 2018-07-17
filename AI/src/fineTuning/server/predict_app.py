from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import os
from flask import Flask, render_template, request
import keras
from keras.preprocessing.image import ImageDataGenerator, load_img 
from keras.models import Model
from keras.models import load_model
import time

# Initialize the Flask application
app = Flask(__name__)
#print (model)
# model = load_model('da_last4_layers.h5')
model = None

#from predict_app import model
@app.route('/hello')
def api_hello():
       return 'Hello John Doe'

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():

    global model
    if model is None:
        model = load_model('da_last4_layers.h5')
    
    background = cv2.imread('background.jpg')

    r = request
    #print r
    #convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    index2result = np.array([1, 0, 1, 1, 1, 1, 0, 0, 1, 0])
    all_class = ['cardboard', 'electronic', 'glass', 'metal', 'paper', 'plastic', 'softplastic',  'tissue paper', 'tools', 'tube' ]

    image_size = 224

    # save original image
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # ##################
    img = cv2.subtract(img, background)

    img_use = cv2.resize(img, (image_size, image_size))
   
    img_use = img_use.reshape((1,) + img_use.shape)
    
    softmax = model.predict(img_use*(1./255))
    predicted_classes = np.argmax(softmax,axis=1)
    # do some fancy processing here....
    print (predicted_classes[0])
    print (all_class[predicted_classes[0]])
    print (softmax[0][predicted_classes[0]])
    cv2.imwrite('saveImg//' + timestr + '_' + all_class[predicted_classes[0]] + '.jpg', img)
    # build a response dict to send back to client
    response = {'result': format(index2result[predicted_classes])[1] } 
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/capture1', methods=['POST'])
def capture1():
    r = request
    #print r
    #convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #image_size = 224

    # save original image
    timestr = time.strftime("%Y%m%d-%H%M%S") + "_C1"
   
    #img = img.reshape((1,) + img.shape)
    
    cv2.imwrite('saveImg//' + timestr + '.jpg', img)
    # build a response dict to send back to client
    response = {'result': format(1) } 
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/capture2', methods=['POST'])
def capture2():
    r = request
    #print r
    #convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #image_size = 224

    # save original image
    timestr = time.strftime("%Y%m%d-%H%M%S") + "_C2"
   
    #img = img.reshape((1,) + img.shape)
    
    cv2.imwrite('saveImg//' + timestr + '.jpg', img)
    # build a response dict to send back to client
    response = {'result': format(1) } 
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/capture0', methods=['POST'])
def capture0():
    r = request
    #print r
    #convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #image_size = 224

    # save original image
    timestr = time.strftime("%Y%m%d-%H%M%S") + "_C0"
   
    #img = img.reshape((1,) + img.shape)
    
    cv2.imwrite('saveImg//' + timestr + '.jpg', img)
    # build a response dict to send back to client
    response = {'result': format(1) } 
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8545)

