from __future__ import print_function

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
import sys
from clienttrash import TrashControlClientTask

import sys

if __name__ == '__main__':
    # t = time.time() 
    print("python demo.py wifi")
    print("python demo.py 0 trash")
    print("python demo.py 1 recycle")
    print("python demo.py 2 nnone")

    print(sys.argv[1]) 
    if sys.argv[1]=="wifi":
        trash = TrashControlClientTask()
        trash.send_blink_led("red","MS_300")
        time.sleep(2)
        #trash.send_turn_off_blink_led()
        trash.send_blink_led("red","MS_50")
        time.sleep(3)
        trash.send_turn_off_blink_led()
        trash.send_led("blue") 
	trash.send_close_cover_case()
	
    key = int(sys.argv[1]) 
    
    if key==0: 
        trash = TrashControlClientTask()
        trash.send_close_cover_case()
        trash.send_go_trash() 
        print ("Go_TRASH_DONE" )
        
    if key==1:
        trash = TrashControlClientTask()
        trash.send_close_cover_case()
        trash.send_go_recycle() 
        print ("go recycle" )

    if key==2:
        trash = TrashControlClientTask()
        trash.send_close_cover_case()
        trash.send_led("red") 
        print ("go none. please press left-right button" )  
    
