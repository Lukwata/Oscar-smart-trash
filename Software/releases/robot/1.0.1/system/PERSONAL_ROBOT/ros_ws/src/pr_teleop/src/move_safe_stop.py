#!/usr/bin/python
import sys
import rospy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist , Pose
from kobuki_msgs.msg import Sound
from kobuki_msgs.msg import Led
from kobuki_msgs.msg import ButtonEvent
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
from kobuki_msgs.msg import PowerSystemEvent
from kobuki_msgs.msg import SensorState
import config
from datetime import datetime


def _callback_pub(message):
    print message
def _error(message):
    print message


class BaseSafeMove(object):
    _vel = Twist()
    _button_pressed = None
    def __init__(self):
        # type: () -> object
        self._do_charing = None #Command()
        rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.BumperEventCallback)
        rospy.Subscriber("/mobile_base/events/wheel_drop", WheelDropEvent, self.WheelDropEventCallback)
        rospy.Subscriber("/mobile_base/events/power_system", PowerSystemEvent, self.PowerEventCallback)
        rospy.Subscriber("/mobile_base/events/button",ButtonEvent,self.ButtonEventCallback)
        self._pr_vel = rospy.Publisher('/pr_base/commands/velocity', String, queue_size=10)


    def start(self):
        self._rate = rospy.Rate(10) # 10hz


    def ButtonEventCallback(self,data):
        if ( data.state == ButtonEvent.RELEASED ) :
            state = "released"
            self.timerange()
        else:
            state = "pressed"
        if ( data.button == ButtonEvent.Button0 ) :
            button = "B0"
            self._button_pressed = datetime.now()
        elif ( data.button == ButtonEvent.Button1 ) :
            button = "B1"
        else:
            button = "B2"
        rospy.loginfo("Button %s was %s."%(button, state))

    def timerange(self):
        pass
        #global CURRENT_TIME
        # tnow = datetime.now()
        # if self._button_pressed != None:
        #     tdelta = tnow - self._button_pressed
        #     seconds = tdelta.total_seconds()
        #     if seconds >= 5 and seconds <=10:
        #         self._deviceModel.factory_reset()
        #         helpers.execute_cmd("sudo reboot",True)
        #     else:
        #         self._button_pressed = None

    def stopMove(self):
            message ='{"cmd":"MOVE", "name": "STOPNOW", "vel":0}'
            self._pr_vel.publish(message)
            self._rate.sleep()

    def BumperEventCallback(self, data):
        feed_status_msg = {"name": "SensorState", "type":"bumper", "value": "0"}
        if (data.state == BumperEvent.RELEASED):
            feed_status_msg = {"name": "SensorState", "type":"bumper", "value": "0", "text":"bumper released"}
            #self.stopMove()
        else:
            feed_status_msg = {"name": "SensorState", "type":"bumper", "value": "1", "text":"bumper pressed"}

        print feed_status_msg
        self.stopMove()


    def WheelDropEventCallback(self, data):
        feed_status_msg = {"name": "SensorState", "type":"WheelDropEvent", "value": "0", "text":"raised"}
        if (data.state == WheelDropEvent.RAISED):
            feed_status_msg = {"name": "SensorState", "type":"WheelDropEvent", "value": "0", "text":"raised"}
            #self.stopMove(feed_status_msg)
        else:
            feed_status_msg = {"name": "SensorState", "type":"WheelDropEvent", "value": "1", "text":"dropped"}
            #self.stopMove(feed_status_msg)
        print feed_status_msg
        self.stopMove()

    def PowerEventCallback(self, data):
        pass
        # self.stopMove()
        # feed_status_msg = {"name": "SensorState", "type":"PowerSystemEvent", "value": "0", "text":""}
        # if (data.event == PowerSystemEvent.UNPLUGGED):
        #     feed_status_msg = {"name": "SensorState", "type":"PowerSystemEvent", "value": "1", "text":"charger unplugged"}
        #
        # elif (data.event == PowerSystemEvent.PLUGGED_TO_ADAPTER):
        #     feed_status_msg = {"name": "SensorState", "type":"PowerSystemEvent", "value": "2", "text":"plugged to adapter"}
        #     self.stopMove(feed_status_msg)
        #
        # elif (data.event == PowerSystemEvent.PLUGGED_TO_DOCKBASE):
        #     feed_status_msg = {"name": "SensorState", "type":"PowerSystemEvent", "value": "3", "text":"plugged to dockbase"}
        #     self.stopMove(feed_status_msg)
        #
        # elif (data.event == PowerSystemEvent.CHARGE_COMPLETED):
        #     feed_status_msg = {"name": "SensorState", "type":"PowerSystemEvent", "value": "4", "text":"charge completed"}
        #     self.stopMove(feed_status_msg)

        #print feed_status_msg

if __name__ == "__main__":
    try:
        rospy.init_node('pr_safe_stop')
        movesafe = BaseSafeMove()
        movesafe.start()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("exception pr_safe_stop was shutdown.")
