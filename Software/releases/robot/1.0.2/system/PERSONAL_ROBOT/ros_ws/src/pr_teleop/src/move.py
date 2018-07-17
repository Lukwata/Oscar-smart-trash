#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String
def movesdk(command):
    pub = rospy.Publisher('/pr_base/commands/velocity', String, queue_size=10)
    rospy.init_node('navigation_move', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #'{"cmd":"MOVE", "name": "%s", "vel": %s}'  % (MOVE , VEL)
    message ='{"cmd":"MOVE", "name": "%s", "vel": %s}'  % (command[1] , command[2])
    print message
    pub.publish(message)
    rate.sleep()

if __name__ == '__main__':
    try:
        #UP, DOWN, LEFT,RIGHT, STOP, VEL
        print sys.argv
        if len(sys.argv) >=3:
            movesdk(sys.argv)
    except rospy.ROSInterruptException:
        pass
