import actionlib
import actionlib_tutorials.msg
import rospy
import navi_services.msg as navimsg
from geometry_msgs.msg import Twist, Pose, Point, Quaternion
from math import radians
import time
from tf import TransformListener, TransformerROS
import copy
import math
import tf_conversions
from kobuki_msgs.msg import BumperEvent

# =================== ROTATION =========================================================================================

def norm_angle(x):
    while x > math.pi:
        x -= 2*math.pi
    while x < -math.pi:
        x += 2*math.pi

    return x


def get_angular_distance(unit1, unit2):

    phi = abs(unit2-unit1) % (math.pi*2)
    sign = 1
    # used to calculate sign
    if not ((unit1-unit2 >= 0 and unit1-unit2 <= math.pi) or (unit1-unit2 <= -math.pi and unit1-unit2 >= -2*math.pi)):
        sign = -1

    if phi > math.pi:
        result = 2*math.pi-phi
    else:
        result = phi

    return result*sign


def call_action_rotation(req):
    client = actionlib.SimpleActionClient('navi_explorer360', navimsg.Explorer360Action)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    if req.angle >=0:
        clockwise = True
        angle = req.angle
    else:
        clockwise = False
        angle=-req.angle
    goal = navimsg.Explorer360Goal(clockwise=clockwise,angle=angle)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    return True


class Explorer360(object):
    # create messages that are used to publish feedback/result
    _feedback = navimsg.Explorer360Feedback()
    _result = navimsg.Explorer360Result()

    def __init__(self):
        self._action_name = "navi_explorer360"
        self._as = actionlib.SimpleActionServer(self._action_name, navimsg.Explorer360Action,
                                                execute_cb=self.execute_explore360, auto_start=False)
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.tf = TransformListener()
        self.pose = Pose()
        self.rot = [0,0,0]
        self._as.start()


    def update_pose(self):
        # current pose
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, quaternion = self.tf.lookupTransform("/base_link", "/map", t)

            self.pose.position.x = position[0]
            self.pose.position.y = position[1]
            self.pose.position.z = position[2]

            self.pose.orientation.x = quaternion[0]
            self.pose.orientation.y = quaternion[1]
            self.pose.orientation.z = quaternion[2]
            self.pose.orientation.w = quaternion[3]

            self.rot = tf_conversions.transformations.euler_from_quaternion(quaternion)

    def execute_explore360(self, goal):
        # helper variables
        hz = 5
        r = rospy.Rate(hz)
        r50 = rospy.Rate(50)
        success = True

        # append the seeds for the fibonacci sequence
        self._feedback.percent = 0.0

        # publish info to the console for the user
        rospy.loginfo('%s: Exploring 360, clockwise=%s angle=%s' % (self._action_name, str(goal.clockwise), str(goal.angle)))

        self.update_pose()
        rot0 = copy.deepcopy(self.rot)
        rot1 = [0,0,0]
        rot2 = [0,0,0]
        if goal.clockwise:
            rot1[2] = norm_angle(rot0[2] + 0.5 * math.pi * float(goal.angle)/180.0)
            rot2[2] = norm_angle(rot0[2] + math.pi * float(goal.angle) / 180.0)
        else:
            rot1[2] = norm_angle(rot0[2] - 0.5 * math.pi * float(goal.angle) / 180.0)
            rot2[2] = norm_angle(rot0[2] - math.pi * float(goal.angle) / 180.0)

        print rot0, rot1, rot2

        #let's turn at 45 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        rotation_speed = 45
        turn_cmd.angular.z = -radians(rotation_speed); #45 deg/s in radians/s
        if not goal.clockwise:
            turn_cmd.angular.z = -turn_cmd.angular.z

        t0 = time.time()
        T = 2.0*360.0/rotation_speed
        state = 2        # 2: far; 1: near; 0: approaching

        pre_dist = 4
        while (time.time() - t0) < T:
            self.cmd_vel.publish(turn_cmd)
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break

            self.update_pose()
            # far
            if state == 2:
                dist = get_angular_distance(self.rot[2], rot1[2])
                if abs(dist)<0.1:
                    state = 1
                    print "from far to near"
            elif state == 1:
                dist = get_angular_distance(self.rot[2], rot2[2])
                if abs(dist) < 0.1:
                    state = 0
                    print "from near to approach the goal"
            else:
                dist = get_angular_distance(self.rot[2], rot2[2])
                if pre_dist * dist <=0:
                    print "pass the goal"
                    break
                #if abs(pre_dist)<abs(dist):
                #    print "pass the goal"
                #    break
                if abs(dist) < 0.01:
                    print "very near the goal"
                    break


            self._feedback.percent = 0
            self._feedback.cur_angle = dist
            self._as.publish_feedback(self._feedback)
            pre_dist = dist
            if state==0:
                r50.sleep()
            else:
                r.sleep()

        # stop rotation
        self.cmd_vel.publish(Twist())

        print time.time()

        self.update_pose()
        print rot0
        print self.rot

        if success:
            self._result.pose = Pose()
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


# =================== MOVE FORWARD =====================================================================================
def call_move_forward(req):
    client = actionlib.SimpleActionClient('navi_move_forward', navimsg.MoveForwardAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = navimsg.MoveForwardGoal(metre=req.metre)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return True


def compute_3d_dist(p1, p2):
    return math.sqrt((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z))


class MoveForwardAction(object):
    # create messages that are used to publish feedback/result
    _feedback = navimsg.MoveForwardFeedback()
    _result = navimsg.MoveForwardResult()

    def __init__(self):
        self._action_name = "navi_move_forward"
        self._as = actionlib.SimpleActionServer(self._action_name, navimsg.MoveForwardAction,
                                                execute_cb=self.execute_move_forward, auto_start=False)
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        #/mobile_base/events/bumper
        rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.bumper_callback)
        self.bumped = False

        self.tf = TransformListener()
        self.pose = Pose()
        self._as.start()

    def bumper_callback(self, bumper_event):
        self.bumped = True

    def update_pose(self):
        # current pose
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, quaternion = self.tf.lookupTransform("/base_link", "/map", t)

            self.pose.position.x = position[0]
            self.pose.position.y = position[1]
            self.pose.position.z = position[2]

            self.pose.orientation.x = quaternion[0]
            self.pose.orientation.y = quaternion[1]
            self.pose.orientation.z = quaternion[2]
            self.pose.orientation.w = quaternion[3]

    def execute_move_forward(self, goal):
        # helper variables
        hz = 5
        r = rospy.Rate(hz)
        r50 = rospy.Rate(50)
        success = False

        # publish info to the console for the user
        rospy.loginfo('%s: Move forward, metre=%s' % (self._action_name, str(goal.metre)))

        # Twist is a datatype for velocity
        move_cmd = Twist()
        # let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.05
        max_v = 0.2
        dist0 = goal.metre
        sign_v = 1
        if goal.metre<0:
            move_cmd.linear.x = - move_cmd.linear.x
            dist0 = -dist0
            sign_v = -1

        # let's turn at 0 radians/s
        move_cmd.angular.z = 0

        self.update_pose()
        pos0 = copy.deepcopy(self.pose.position)

        T = 5.0 * dist0 / max_v # seconds
        if T<10:       # timeout = 10 seconds
            T = 10
        t0 = time.time()
        dist = compute_3d_dist(pos0, self.pose.position)
        pre_dist = dist

        state = 2       # 2: far; 1: near; 0: approaching the goal
        self.bumped = False
        while ((time.time() - t0) < T) and (not self.bumped):
            self.cmd_vel.publish(move_cmd)
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break

            self.update_pose()
            dist = compute_3d_dist(pos0, self.pose.position)

            if state == 2:
                if abs(move_cmd.linear.x) < max_v:
                    new_v = abs(dist) + 0.01
                    if new_v > max_v:
                        new_v = max_v
                    if new_v > abs(move_cmd.linear.x):
                        move_cmd.linear.x = new_v * sign_v
                    #print "new_v", new_v

                if dist>dist0/2:
                    print "far ==> near"
                    state = 1
            elif state == 1:
                if abs(dist0-dist)<0.3:
                    print "near ==> approaching the goal"
                    state = 0
            elif state == 0:
                new_v = abs(dist0-dist) + 0.01
                if new_v < abs(move_cmd.linear.x):
                    move_cmd.linear.x = new_v * sign_v
                #print move_cmd.linear.x

                if abs(dist0-dist)<0.01:
                    print "very near the goal"
                    success = True
                    break
                elif dist >= dist0:
                    print "pass the goal"
                    break

            self._feedback.percent = 0
            self._as.publish_feedback(self._feedback)
            pre_dist = dist
            if state==0:
                r50.sleep()
            else:
                r.sleep()

        #=======================
        self.update_pose()
        self.cmd_vel.publish(Twist())
        self._result.pose = self.pose
        if success:
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
