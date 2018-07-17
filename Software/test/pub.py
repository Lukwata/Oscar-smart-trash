import zmq
import time


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("ipc:///tmp/brain_zmq_sensor_pub_sub")
time.sleep(3)


socket.send_string("af30747d-4135-11e7-a20e-a45e60c90f49", zmq.SNDMORE)
socket.send_json({"source": "", "type": "check_internet", "data": {"action": "on"}})

# //socket.send("%s %s" % ("B", "gsgsdgsdgd"))

time.sleep(5)