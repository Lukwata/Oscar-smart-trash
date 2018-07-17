import time
import zmq
import json
import sys
import rospy
import cv2
from datetime import datetime
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

ZMQ_CHANNEL = "ipc:///tmp/autonomous_camera"
CAMERA_COMMAND_TAKE_PICTURE = "take_picture"


class ImageCapturer:

    def __init__(self):
        print 'init'
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rgb/image", Image, self.image_callback)

    def image_callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        (rows, cols, channels) = self.cv_image.shape

    def save_image(self):
        time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        img_path = "/tmp/{}.jpg".format(time)
        cv2.imwrite(img_path, self.cv_image)
        return img_path

ic = ImageCapturer()
rospy.init_node("camera_zmq", anonymous=True)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(ZMQ_CHANNEL)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    try:
        print "Before socket.recv(): "
        message = socket.recv()
        print "Received request: ", message
        path = ic.save_image()
        s = {"path": path}
        socket.send(json.dumps(s))
    except Exception:
        break

    rate.sleep()
