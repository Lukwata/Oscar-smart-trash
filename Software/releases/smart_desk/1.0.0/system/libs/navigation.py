#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import zmq
import time
from aos.system.libs.util import Util
import sys
import rospy
from std_msgs.msg import String
velocity = 2.5

class Navigation:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    # init Navigation Object
    def __init__(self, addr="ipc:///tmp/navi_bridge_default.ipc", info_addr="ipc:///tmp/Task_Pub_Info.ipc"):
        self.context = zmq.Context.instance()
        self.cmd_socket = self.context.socket(zmq.REQ)
        self.cmd_socket.connect(addr)
        self.info_socket = self.context.socket(zmq.SUB)
        self.info_socket.setsockopt(zmq.SUBSCRIBE, "")
        self.info_addr = info_addr
        self.info_poller = zmq.Poller()
        self.task_id = None
        self.status = None

    def parse_info(self, s):
        d = s.split(":")
        if len(d) != 3:
            print "ERROR: Navigation E0001: Parse message from info channel ", s
            return None
        try:

            task_id = int(d[0])
            status = int(d[1])
            timestamp = float(d[2])
            return {"task_id": task_id, "status": status, "timestamp": timestamp}
        except:
            print "ERROR: Navigation E0002: Parse message from info channel ", s
            return None

    # send_cmd{}
    # input cmd  { Navigation.go_forward_cmd(2) }
    # return task_id
    def send_cmd(self, cmd):
        if not isinstance(cmd,dict):
            print "ERROR: not json format", cmd
            self.task_id = -1
            return self.task_id

        self.cmd_socket.send_json(cmd)
        self.task_id = self.cmd_socket.recv()
        print "task_id: ", self.task_id
        return self.task_id

    # send_cmd_and_wait{}
    # input cmd  { Navigation.go_forward_cmd(2) }
    # input timeout seconds
    # return status {True, False}
    def send_cmd_and_wait(self, cmd, timeout=0):

        self.info_socket.connect(self.info_addr)
        self.info_poller.register(self.info_socket, zmq.POLLIN)

        task_id_str = self.send_cmd(cmd)
        task_id = int(task_id_str)

        t0 = time.time()
        status = False
        while True:
            if timeout == 0:
                remain_time = 1000
            else:
                remain_time = (t0 + timeout - time.time()) * 1000        # in millisecond
            if remain_time<0:
                print "timeout"
                break
            socks = dict(self.info_poller.poll(remain_time))
            if self.info_socket in socks:
                msg = self.info_socket.recv()
                print "feedback from TaskQueue: ", msg
                data = self.parse_info(msg)
                if data is not None:
                    if data["task_id"] > task_id:  # DONE
                        status = True
                        break
                    if data["task_id"] == task_id:  # DOING
                        if data["status"] == Navigation.DONE:
                            status = True
                            break
                        elif data["status"] == Navigation.DOING:
                            print "Doing the task"
                        else:
                            print data
                    if data["task_id"] < task_id:  # DOING
                        print "task is in waiting list"

        self.info_poller.unregister(self.info_socket)
        self.info_socket.setsockopt(zmq.LINGER, 0)
        self.info_socket.disconnect(self.info_addr)
        return status

    # rotation_cmd{}
    # input angle {0-360}
    @staticmethod
    def rotation_cmd(angle):
        return {"action":"rotate", "angle":angle}

    # go_forward_cmd{}
    # input metre { int }
    @staticmethod
    def go_forward_cmd(metre):
        return {"action":"go_forward", "metre": metre}

    @staticmethod
    def stop_cmd():
        return {"action":"stop"}

    @staticmethod
    def stop_all_cmd():
        return {"action": "stop_all"}

    @staticmethod
    def auto_docking_cmd():
        return {"action": "auto_docking"}

    @staticmethod
    def goto_xy_cmd(x,y):
        return {"action": "goto_xy", "x": x, "y": y}

    # define function.
    def go_forward(self,metre):
        self.send_cmd( Navigation.go_forward_cmd(metre))

    def rotate(self,angle):
        self.send_cmd( Navigation.rotation_cmd(angle))

    def stop(self):
        self.send_cmd(Navigation.stop_cmd())

    def stop_all(self):
        self.send_cmd(Navigation.stop_all_cmd())

    def auto_docking(self):
        self.send_cmd(Navigation.auto_docking_cmd())

    def goto_xy(self, x, y):
        self.send_cmd(Navigation.goto_xy_cmd(x,y))


class MobileBase:
    def __init__(self):
        super(MobileBase, self).__init__()

    @staticmethod
    def go_forward():
        MobileBase.runAction("UP",velocity)

    @staticmethod
    def go_back():
        MobileBase.runAction("DOWN",velocity)

    @staticmethod
    def rotate_left():
        MobileBase.runAction("LEFT",0)

    @staticmethod
    def rotate_right():
        MobileBase.runAction("RIGHT",0)
        pass

    @staticmethod
    def stop():
        MobileBase.runAction("STOP",0)
        pass

    @staticmethod
    def stop_now():
        MobileBase.runAction("STOPNOW",0)
        pass

    @staticmethod
    def go_to(x,y):
        pass

    @staticmethod
    def runAction(MOVE,VEL):
        try:
            # pub = rospy.Publisher('/pr_base/commands/velocity', String, queue_size=10)
            # rospy.init_node('navigation_move', anonymous=True)
            # rate = rospy.Rate(10)# 10hz
            # message ='{"cmd":"MOVE", "name": "%s", "vel": %s}'  % (MOVE , VEL)
            # pub.publish(message)
            # rate.sleep()
            Util.cmd("source ~/set_params.sh; python ~/aos/system/PERSONAL_ROBOT/ros_ws/src/pr_teleop/src/move.py %s %s" % (MOVE,VEL) )

        except Exception as ex:
            print "error MobileBase " + str(ex.message)


###################TEST Example ############################
'''
# import class
from aos.system.libs.navigation import MobileBase, Navigation
# Packages loaded
# MobileBase
MobileBase.go_forward() # robot se di chuyen ve phia truoc den khi nao ban goi stop.
MobileBase.go_back() #
MobileBase.rotate_left()
MobileBase.rotate_right()
MobileBase.stop() #  Robot se dung lai cac action forward, back, left,right phai tren.
MobileBase.stop_now() # stop ngay lap tuc.


# Navigation
# Neu ban dang su dung class MobileBase de di chuyen, vui long goi MobileBase.stop() truoc khi su dung Navigation de dieu khien robot.

MobileBase.stop() #  Robot stop truoc khi su dung Navigation class.
# init class
Nav  = Navigation()

#param: metre (met')  metre >0 robot di ve phia truoc. metre < 0 robot di ve phia sau.
Nav.go_forward(metre)

# rotate:  angle , -360(trai) < angle < 360 (phai)
Nav.rotate(angle)

# AutoDocking Charge. Robot phai o gan vi tri Dockcharge
Nav.auto_docking()

#go_to_xy . x,y la toa do vi tri tren ban do.
Nav.goto_xy(x,y)

# cancel action dang thuc thi.
Nav.stop()

# cancel tat ca cac action
Nav.stop_all()
'''
