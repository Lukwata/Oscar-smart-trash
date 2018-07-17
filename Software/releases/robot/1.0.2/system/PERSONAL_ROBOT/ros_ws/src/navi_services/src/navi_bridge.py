import zmq
import time
import sys
import os
import json

import threading
import subprocess

import Queue
import actionlib
import navi_services.msg as navimsg
from kobuki_msgs.msg import AutoDockingAction, AutoDockingGoal
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion
from actionlib_msgs.msg import *
import rospy
from tf import TransformListener


_version = "0.1.0"
_tcp_addr = "tcp://*:10000"
_addr = "ipc:///tmp/navi_bridge_default.ipc"

_tcp_pub_addr = "tcp://*:10001"
_pub_addr = "ipc:///tmp/navi_bridge_pub_default.ipc"


_info = "starting navi_bridge" \
        "\n 21-Nov-2016: support both tcp and ipc" \
        "\n 15-Mar-2017: support pub/sub channel for returning status/info"


def print_info():
    print "="*10, "navi_bridge", "="*10
    print "+ version ", _version
    print "+ note: ", _info
    print "=" * 33


def show_clock():
    sys.stdout.write("Time: %s   \r" % (time.ctime()))
    sys.stdout.flush()


def normalize_msg(m):
    try:
        if isinstance(m,str):
            mj = json.loads(m)

        if isinstance(mj, dict):
            if mj.has_key("action"):
                return mj
            mj["action"] = "none"
            return mj
    except:
        print "ERROR 0003: cannot normalize message"
    return {"action":"none", "msg": m}


def str2float(s):
    if not isinstance(s, float):
        try:
            s = float(s)
        except:
            print "Cannot convert to float"
            print s
            s = 0
    return s

# =========================================================================
def create_action(task):
    if task["action"] == "rotate":
        if task.has_key("angle"):
            angle = int(str2float(task["angle"]))
            if angle != 0:
                return RotationAction(angle)

    if task["action"] == "go_forward":
        if task.has_key("metre"):
            metre = str2float(task["metre"])
            if metre != 0:
                return GoForwardAction(metre)

    if task["action"] == "map_cmd":
        if task.has_key("cmd"):
            return MapCmd(task["cmd"])

    if task["action"] == "auto_docking":
        return BridgeAutoDockingAction()

    if task["action"] == "explorer":
        return ExplorerCmd(task["cmd"])

    if task["action"] == "goto_xy":
        if task.has_key("x") and task.has_key("y"):
            x = str2float(task["x"])
            y = str2float(task["y"])
            timeout = 60
            if task.has_key("timeout"):
                timeout = str2float(task["timeout"])
            return GotoXYAction(x,y,timeout)


    return NullAction()


# =========================================================================
class ExplorerCmd:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self, cmd):
        self.cmd = cmd
        self.is_running = False
        self.status = ExplorerCmd.NONE
        pass

    def run(self):
        self.status = ExplorerCmd.DOING
        if self.cmd == "start":
            subprocess.call(["rosservice","call","/rtabmap/set_mode_mapping"])
            subprocess.call(["tmux new-window -n auto_navi -d"],shell=True)
            subprocess.call(["tmux send-keys -t navi:auto_navi.0 'source ~/set_params.sh; roslaunch explorer simple_navigation_turtlebot.launch' C-m"], shell=True)
        if self.cmd == "stop":
            subprocess.call(["tmux kill-window -t navi:auto_navi"], shell=True)
            subprocess.call(["rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}"], shell=True)
            subprocess.call(["rosservice","call","/rtabmap/set_mode_localization"])
            

        self.status = ExplorerCmd.DONE

    def close(self):
        print "Closing ExplorerCmd class"

    def stop(self):
        self.is_running = False
        while self.status != ExplorerCmd.DONE:
            time.sleep(0.1)

# =========================================================================
class MapCmd_V1:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self, cmd):
        self.cmd = cmd
        self.is_running = False
        self.status = MapCmd.NONE
        pass

    def run(self):
        self.status = MapCmd.DOING
        if self.cmd == "set_mode_mapping":
            subprocess.call(["rosservice","call","/rtabmap/set_mode_mapping"])
        if self.cmd == "set_mode_localization":
            subprocess.call(["rosservice","call","/rtabmap/set_mode_localization"])
        if self.cmd == "reset":
            subprocess.call(["rosservice","call","/rtabmap/reset"])

        self.status = MapCmd.DONE

    def close(self):
        print "Closing MapCmd class"

    def stop(self):
        self.is_running = False
        while self.status != MapCmd.DONE:
            time.sleep(0.1)

# =========================================================================
class MapCmd:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3
    
    msg = """ Control Your Turtlebot! """
	
    def __init__(self, cmd):
        self.cmd = cmd
        self.is_running = False
        self.status = MapCmd.NONE
        pass

    def run(self):
	    rospy.init_node('turtlebot_teleop')
            pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5)
            print(msg)	
           		
	    while(1):
                  twist = Twist()
            	  twist.linear.x = 0.1; twist.linear.y = 0; twist.linear.z = 0
            	  twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            	  pub.publish(twist)  
           
            self.status = MapCmd.DONE

    def close(self):
        print "Closing MapCmd class"

    def stop(self):
        self.is_running = False
        while self.status != MapCmd.DONE:
            time.sleep(0.1)
# =========================================================================
class GotoXYAction:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self, x, y, timeout=60):
        self.pos = [x, y, 0]
        self.quat = [0.0, 0.0, 0.0, 1.0]
        self.timeout = timeout

        self.status = GotoXYAction.NONE
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

    def run(self):
        print "GotoXYAction is running ..."
        self.status = GotoXYAction.DOING

        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(self.pos[0], self.pos[1], self.pos[2]),
                                     Quaternion(self.quat[0], self.quat[1], self.quat[2], self.quat[3]))

        self.client.send_goal(goal)
        success = self.client.wait_for_result(rospy.Duration(self.timeout))

        state = self.client.get_state()

        if success and state == GoalStatus.SUCCEEDED:
            print "reached the desired pose"
        else:
            print "The base failed to reach the desired pose. State = ", state

            if state != GoalStatus.PREEMPTED:
                self.client.cancel_goal()

        self.status = RotationAction.DONE

    def close(self):
        print "Closing GotoXYAction"

    def stop(self):
        self.client.cancel_goal()
        print "Stoping GotoXYAction"

# =========================================================================
class BridgeAutoDockingAction:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self):
        self.status = BridgeAutoDockingAction.NONE
        self.client = actionlib.SimpleActionClient('dock_drive_action', AutoDockingAction)
        self.client.wait_for_server()

    def run(self):
        print "BridgeAutoDockingAction is running ..."
        self.status = BridgeAutoDockingAction.DOING

        goal = AutoDockingGoal()
        self.client.send_goal(goal)
        self.client.wait_for_result()

        self.status = RotationAction.DONE

    def close(self):
        print "Closing BridgeAutoDockingAction"

    def stop(self):
        self.client.cancel_goal()
        print "Stoping BridgeAutoDockingAction"

# =========================================================================
class NullAction:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self):
        self.is_running = False
        self.status = NullAction.NONE
        pass

    def run(self):
        self.status = NullAction.DONE

    def close(self):
        print "Closing NullAction class"

    def stop(self):
        self.is_running = False
        while self.status != NullAction.DONE:
            time.sleep(0.1)


# =========================================================================
class RotationAction:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self, angle):
        self.angle = angle
        self.status = RotationAction.NONE
        self.client = actionlib.SimpleActionClient('navi_explorer360', navimsg.Explorer360Action)
        self.client.wait_for_server()

    def run(self):
        print "RotationAction is running ..."
        self.status = RotationAction.DOING
        if self.angle >= 0:
            clockwise = True
            angle = self.angle
        else:
            clockwise = False
            angle = -self.angle
        goal = navimsg.Explorer360Goal(clockwise=clockwise, angle=angle)
        self.client.send_goal(goal)
        self.client.wait_for_result()

        self.status = RotationAction.DONE

    def close(self):

        print "Closing RotationAction"

    def stop(self):
        self.client.cancel_goal()
        print "Stoping RotationAction"

# =========================================================================
class GoForwardAction:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self, metre):
        self.metre = metre
        self.status = GoForwardAction.NONE
        self.client = actionlib.SimpleActionClient('navi_move_forward', navimsg.MoveForwardAction)
        self.client.wait_for_server()

    def run(self):
        print "RotationAction is running ..."
        self.status = GoForwardAction.DOING

        goal = navimsg.MoveForwardGoal(metre=self.metre)
        self.client.send_goal(goal)
        self.client.wait_for_result()

        self.status = GoForwardAction.DONE

    def close(self):
        print "Closing GoForwardAction"

    def stop(self):
        self.client.cancel_goal()
        print "Stoping GoForwardAction"
# =========================================================================

class TaskStatus:
    NONE = 0
    WAITING = 1
    DOING = 2
    DONE = 3

    def __init__(self):
        pass


class TaskQueue:
    def __init__(self, task_pub_addr="ipc:///tmp/Task_Pub_Info.ipc"):
        self.task_pub_addr = task_pub_addr
        self.context = zmq.Context.instance()
        self.pub_sock = self.context.socket(zmq.PUB)
        self.pub_sock.bind(self.task_pub_addr)

        self.task_count = 0
        self.reset_task_queue = False
        self.cur_task = None
        self.cur_task_id = 0
        self.cur_status = TaskStatus.NONE
        self.thread_id = threading.Thread(target=self.execute_cmd)
        self.queue = Queue.Queue()
        self.task_lock = threading.Lock()

        self.thread_id.start()

    def pub_status(self):
        self.pub_sock.send(str(self.cur_task_id) + ":" + str(self.cur_status) + ":" + str(time.time()))

    def execute_cmd(self):
        while not rospy.is_shutdown():
            if self.reset_task_queue:
                while self.queue.qsize()>0:
                    self.queue.get()
                self.reset_task_queue = False

            elif self.queue.qsize()>0:
                task = self.queue.get()
                self.task_lock.acquire()
                self.cur_task_id = task["task_id"]
                self.cur_status = TaskStatus.DOING
                self.pub_status()
                self.cur_task = create_action(task)
                self.task_lock.release()

                print "execute ", task
                self.cur_task.run()

                print "done", task
                self.cur_task.close()

                self.task_lock.acquire()
                self.cur_status = TaskStatus.DONE
                self.pub_status()
                self.task_lock.release()
            else:
                show_clock()
                time.sleep(0.1)

    def append_new_task(self, msg):
        self.task_count += 1
        msg["task_id"] = self.task_count
        self.queue.put(msg)
        print "Appending new task ", msg
        return msg["task_id"]

    def stop_cur_task(self):
        self.task_lock.acquire()
        if self.cur_status == TaskStatus.DOING:
            self.cur_task.stop()
        self.task_lock.release()


    def stop_all_tasks(self):
        self.reset_task_queue = True
        while self.queue.qsize()>0:
            self.stop_cur_task()
            time.sleep(0.1)


# =====================================================================================================================
def get_robot_pose_xy():

    if global_tf.frameExists("/base_link") and global_tf.frameExists("/map"):
        t = global_tf.getLatestCommonTime("/map", "/base_link")
        pos, quat = global_tf.lookupTransform("/map", "/base_link", t)
        return pos[0], pos[1]
    else:
        print "Cannot get transform from map to base_link"
        return 0, 0


def query_info(msg):
    if msg.has_key("what"):
        if msg["what"] == "ROBOT_POSE":
            x, y = get_robot_pose_xy()
            out = {'x':x, 'y':y}
            return json.dumps(out)

    return ""


def query_list_labels():
    list_labels = []


    return json.dumps({"action":"get_list_labels","list_labels":list_labels})


def set_label(msg):
    if msg.has_key("label"):
        label = "'" + msg["label"] + "'"
        subprocess.call(["rosservice", "call", "/rtabmap/set_label", "0", label])


def goto_label(msg):
    if msg.has_key("label"):
        label = "'" + msg["label"] + "'"
        print ("go to " + label)
        cmd = ["rosservice", "call", "/rtabmap/set_goal", "0", label]
        print (cmd)
        subprocess.call(cmd)
        print ("reached " + label)


def publish_msg(tag, data):
    msg = tag + ":" + data
    pub_socket.send_string(msg)
    pub_tcp_socket.send(msg)


if __name__ == "__main__":
    print_info()

    rospy.init_node('navi_bridge_node')
    print "Ready"

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.LINGER, 0)
    socket.bind(_addr)

    tcp_socket = context.socket(zmq.REP)
    tcp_socket.setsockopt(zmq.LINGER, 0)
    tcp_socket.bind(_tcp_addr)

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    poller.register(tcp_socket, zmq.POLLIN)

    pub_socket = context.socket(zmq.PUB)
    socket.bind(_pub_addr)

    pub_tcp_socket = context.socket(zmq.PUB)
    pub_tcp_socket.bind(_tcp_pub_addr)

    tasks = TaskQueue()

    global_tf = TransformListener()

    while not rospy.is_shutdown():
        #  Wait for next request from client
        try:
            socks = dict(poller.poll(1000))
            sock = None
            if socket in socks and socks[socket] == zmq.POLLIN:
                sock = socket
            elif tcp_socket in socks and socks[tcp_socket] == zmq.POLLIN:
                sock = tcp_socket
            if sock is not None:
                message = sock.recv()
                print "Received request: ", message
                norm_msg = normalize_msg(message)

                print "norm", norm_msg
                if norm_msg["action"] == "stop_all":
                    tasks.stop_all_tasks()
                    sock.send("0")
                elif norm_msg["action"] == "stop":
                    tasks.stop_cur_task()
                    sock.send("0")
                elif norm_msg["action"] == "get_info":
                    info = query_info(norm_msg)
                    sock.send(info)
                elif norm_msg["action"] == "get_list_labels":
                    info = query_list_labels()
                    sock.send(info)
                elif norm_msg["action"] == "set_label":
                    set_label(norm_msg)
                    sock.send("0")
                elif norm_msg["action"] == "goto_label":
                    goto_label(norm_msg)
                    sock.send("0")
                elif norm_msg["action"] != "none":
                    task_id = tasks.append_new_task(norm_msg)
                    sock.send(str(task_id))
                else:
                    sock.send("-1")
                    print "ERROR 0002: no action"
        except:
            print "ERROR 0001"
            break


    print "exiting"

    os._exit(0)
