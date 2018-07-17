#!/usr/bin/env python
#
# File:   desk_control.py
# Author: Hoang Phuong
#
# Created on September 24, 2015, 17:10 PM
#
import json
from time import sleep
import struct
import zmq
from aos.system.libs.notify import Notify
from aos.system.configs.channel import CURRENT_PATH
from aos.system.libs.util import Util


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class SmartTrashControl(object):
    __metaclass__ = Singleton
    _socket_req = None

    def __init__(self):
        if self._socket_req is None:
            url_socket = "ipc:///tmp/desk_control:9999"
            c = zmq.Context()

            socket_req = c.socket(zmq.REQ)
            socket_req.connect(url_socket)
            socket_req.setsockopt(zmq.RCVTIMEO, 500)

            print "desk client control url socket: " + url_socket
            self._socket_req = socket_req

    def turnLeft():
        pass
    def turnRight():
        pass
    def closeMain():
        pass
    def controlLed(ledNumber, status):
        pass 

   
