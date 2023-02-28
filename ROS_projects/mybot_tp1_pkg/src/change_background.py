#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_srvs.srv import Empty


if __name__ == '__main__':
    try:
        
        if rospy.has_param('red_color') : old_red = rospy.get_param('red_color')
        else :                            old_red = False

        # initialise a new ROS node with name mybot_color;
        rospy.init_node('change_bg')

        # create a service client to call the clear service of turtlesim
        clear_bg = rospy.ServiceProxy('/clear', Empty)

        rate = rospy.Rate(10)

        while not rospy.is_shutdown() :

            new_red = rospy.get_param('red_color')

            change = new_red != old_red
            old_red = new_red

            if change and new_red :
                rospy.set_param('/simScreen/background_r', 130)
                rospy.set_param('/simScreen/background_g', 130)
                rospy.set_param('/simScreen/background_b', 130)
                clear_bg()
            elif change and not(new_red) :
                rospy.set_param('/simScreen/background_r', 69)
                rospy.set_param('/simScreen/background_g', 155)
                rospy.set_param('/simScreen/background_b', 86)
                clear_bg()
            
            rate.sleep()
        


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