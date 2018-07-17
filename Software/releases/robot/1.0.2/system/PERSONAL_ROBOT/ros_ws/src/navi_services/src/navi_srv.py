#!/usr/bin/env python

import rospy
from navi_services.srv import *
import actionlib
from pr_explorer import Explorer360, call_action_rotation, MoveForwardAction, call_move_forward


def start_services():
    print "===Start services======="
    print "navi_service_rotation"
    rospy.Service('navi_service_rotation', Rotation, call_action_rotation)
    print "navi_service_move_forward"
    rospy.Service('navi_service_move_forward', MoveForward, call_move_forward)
    print "========================"



def start_actions():
    print "==Start action services=="

    Explorer360()
    MoveForwardAction()

    print "========================="


if __name__ == "__main__":
    rospy.init_node('navi_services_node')

    start_services()
    start_actions()

    rospy.spin()