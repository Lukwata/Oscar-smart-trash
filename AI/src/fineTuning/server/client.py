import requests
import json
#import cv2

addr = 'http://localhost:8545'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

#img = cv2.imread('test2.jpg')
img = open('test2.jpg', 'rb').read()
# encode image as jpeg
#_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img, headers=headers)
# decode response
print (json.loads(response.text))

# expected output: {u'message': u'image received. size=124x124'}
