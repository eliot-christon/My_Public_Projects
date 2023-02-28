#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from std_msgs.msg import Bool



def change_color(is_red):
    if is_red:
        set_pen_handle(200, 0, 0, 4, False)

    else :
        set_pen_handle(179, 184, 255, 3, False)


def close_to_border(x, y):
    return (x < 1 or x > 10 or y < 1 or y > 10)



# Callback function for reading turtlesim node output
def read_pose_callback(msg):
    global old_red
    new_red = close_to_border(msg.x,msg.y)
    if (old_red != new_red) : 
        change_color(new_red)
        old_red = new_red
        # rospy.set_param('red_color', new_red) # for change_background.py
        bg_pub.publish(new_red) # for change_background2.py


if __name__ == '__main__':
    try:
        
        old_red = False

        if not(rospy.has_param('teleop_turtle_name')) : rospy.set_param('teleop_turtle_name', '/turtle1')
        rospy.set_param('red_color', old_red)

        pose_name = str(rospy.get_param('teleop_turtle_name'))+'/pose'
        set_pen_name = str(rospy.get_param('teleop_turtle_name'))+'/set_pen'

        # initialise a new ROS node with name mybot_color;
        rospy.init_node('mybot_color')

        rospy.wait_for_service(set_pen_name)
        set_pen_handle = rospy.ServiceProxy(set_pen_name,SetPen)


        bg_pub = rospy.Publisher("bg_color", Bool, queue_size=10)
        # define a subscriber on the /turtle1/pose topic with the imported data type on the step before together
        # with a callback function which will be run each time a new data is present on the subscribed topic;
        subscriber = rospy.Subscriber(pose_name, Pose, read_pose_callback)
        

        # And then ... wait for the node to be terminated
        rospy.spin()

    except rospy.ROSInterruptException:
        pass



""" OLD

def change_color(is_red=True):
    
    pen_request = SetPenRequest()
    
    if is_red:
        pen_request.r = 200
        pen_request.g = 0
        pen_request.b = 0
        pen_request.width = 4
        set_pen_handle(pen_request)

    else :
        pen_request.r = 179
        pen_request.g = 184
        pen_request.b = 255
        pen_request.width = 3
        set_pen_handle(pen_request)


"""