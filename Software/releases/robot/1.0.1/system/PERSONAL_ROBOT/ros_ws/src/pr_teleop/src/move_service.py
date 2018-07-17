#!/usr/bin/python
import sys
import rospy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist , Pose
from kobuki_msgs.msg import Sound
from kobuki_msgs.msg import Led
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
from kobuki_msgs.msg import PowerSystemEvent
from kobuki_msgs.msg import SensorState
#import helpers
import json
import config
from datetime import datetime


CURRENT_VEL  = Twist()
COMMAND_MOVE_LAST = Twist()
FN_MOVE_DONE = True
VEL_CURENT_LEVEL = 0.0

class MoveService(object):
    _vel = Twist()
    #_deviceModel = None
    #_pubnub = Pubnub(config.PUB_KEY, config.SUB_KEY)
    _charged_status = 0
    _base_mode = 0
    _rate = None
    def __init__(self):
        # type: () -> object
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.vel_sub = rospy.Subscriber('/pr_base/commands/velocity', String, self.callback_velocity_sub )
        self._rate = rospy.Rate(10) # 10hz

    def start(self):
        global CURRENT_VEL
        global FN_MOVE_DONE
        self._vel = Twist()
        countZero = 0
        while True:
            self._vel = CURRENT_VEL
            if self._vel.linear.x == 0 and self._vel.angular.z == 0:
                if countZero < 2:
                    self.vel_pub.publish(self._vel)
                    self._rate.sleep()
                    countZero = countZero +1
                    print "pub vel count zerro"
            else:
                countZero = 0
                self.vel_pub.publish(self._vel)
                self._rate.sleep()
                print "pub vel"

            self._rate.sleep()
    def _stop_vel(self):
        vel = Twist()
        vel.linear.x = 0.0
        return vel
    #=========================
    def _move(self, vel_goal, vel_stop_now):
        print "_move"
        global FN_MOVE_DONE
        global CURRENT_VEL

        FN_MOVE_DONE = False
        CURRENT_VEL.angular.z = vel_goal.angular.z
        while float(CURRENT_VEL.linear.x) != float(vel_goal.linear.x):
            if CURRENT_VEL.linear.x > vel_goal.linear.x:
                CURRENT_VEL.linear.x = float(max(CURRENT_VEL.linear.x - 0.01, vel_goal.linear.x))

            if CURRENT_VEL.linear.x < vel_goal.linear.x:
                CURRENT_VEL.linear.x = float(min(CURRENT_VEL.linear.x + 0.01, vel_goal.linear.x))
            time.sleep(0.1)
            CURRENT_VEL.linear.x = float(CURRENT_VEL.linear.x)
        time.sleep(0.1)
        FN_MOVE_DONE = True


    def callback_velocity_sub(self,message):
        global FN_MOVE_DONE
        global COMMAND_MOVE_LAST
        global VEL_CURENT_LEVEL
        global CURRENT_VEL
        print message
        print message.data
        try:
            message = json.loads(message.data)
            if message['cmd'] == config.CMD_MOVE  :
                #COMMAND_MOVE_LAST = Twist()
                vel = Twist()
                vel.linear.x = self._vel.linear.x
                vel.angular.z = self._vel.angular.z

                linear_x = float( message["vel"]) * 0.1

                if message['name'] == "UP":
                    if float(vel.angular.z) != 0:
                        vel.angular.z = 0
                    vel.linear.x = min(linear_x , config.BASE_VEL_MAX_UP)

                if message['name'] == "DOWN":
                    if float(vel.angular.z) != 0:
                        vel.angular.z = 0
                    linear_x = float( message["vel"]) * 0.1 * (-1)
                    vel.linear.x = max(linear_x , config.BASE_VEL_MAX_DOWN)


                if message['name'] == "LEFT":
                    vel.angular.z = min(vel.angular.z + 0.7, 0.7)
                    vel.linear.x = 0

                if message['name'] == "RIGHT":
                    vel.angular.z = max(vel.angular.z - 0.7, -0.7)
                    vel.linear.x = 0

                if message['name'] == "STOP":# STOP
                    vel = Twist()

                if message['name'] == "STOPNOW":# STOP
                    print "stop_now"
                    CURRENT_VEL = Twist()
                    vel = Twist()
                ####===sent...
                if FN_MOVE_DONE ==True:
                    self._move(vel,False)


                # if FN_MOVE_DONE ==True:
                #     self._move(COMMAND_MOVE_LAST)

            # if message['name'] == config.CMD_AUTO_CHARGE:
            #     self._move(self._stop_vel())
            #     time.sleep(5)
            #     if(self._charged_status == 0):
            #         #self._do_charing = Command("roslaunch kobuki_auto_docking activate.launch")
            #         #self._do_charing.run()
            #         #self._charged_status = 1
            #         #command.terminate()
            #         break;
            #
            # if message['name'] == config.CMD_REMOVE_AUTO_CHARGE_MODE:
            #     self._move(self._stop_vel())
            #     time.sleep(5)
            #     self._do_charing.terminate()
            #     self._charged_status = 0

        except Exception as err:
            print err

if __name__ == "__main__":
    try:
        rospy.init_node('pr_move_node')
        move = MoveService()
        move.start()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("exception move service was shutdown.")
