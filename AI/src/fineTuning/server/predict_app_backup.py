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
        
    r = request
    #print r
    #convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    index2result = np.array([1, 0, 1, 1, 1, 1, 0, 0, 1, 0])
    image_size = 224
    img = cv2.resize(img, (image_size, image_size))
    img = img.reshape((1,) + img.shape)
        
    softmax = model.predict(img*(1./255))
    predicted_classes = np.argmax(softmax,axis=1)
    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'result': format(index2result[predicted_classes])[1] } 
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8545)

