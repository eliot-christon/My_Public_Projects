#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_srvs.srv import Empty
from std_msgs.msg import Bool



def change_bg_callback( msg ):

    if 'True' in str(msg):
        rospy.set_param('/simScreen/background_r', 130)
        rospy.set_param('/simScreen/background_g', 130)
        rospy.set_param('/simScreen/background_b', 130)

    else :
        rospy.set_param('/simScreen/background_r', 69)
        rospy.set_param('/simScreen/background_g', 155)
        rospy.set_param('/simScreen/background_b', 86)
    
    clear_bg()


if __name__ == '__main__':
    try:

        rospy.wait_for_service('/clear')
        clear_bg = rospy.ServiceProxy('/clear', Empty)
        rospy.wait_for_service('/clear')

        # initialise a new ROS node with name mybot_color;
        rospy.init_node('change_bg')

        # create a service client to call the clear service of turtlesim
        rospy.Subscriber("bg_color", Bool, change_bg_callback) # same topic name as the publisher

        # set a green bg
        change_bg_callback( 'False' )

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