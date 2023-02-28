#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import sys, termios, tty
import click
from geometry_msgs.msg import Twist


# Arrow keys codes
keys = {'\x1b[A':'up', '\x1b[B':'down', '\x1b[C':'right', '\x1b[D':'left', 'w':'quit', \
    'z':'up', 's':'down', 'q':'left', 'd':'right', 'a':'lin_acc', 'e':'lin_dec', 'r':'ang_acc', 'f':'ang_dec', 'x':'stop'}


if not(rospy.has_param('teleop_turtle_name')) : rospy.set_param('teleop_turtle_name', '/turtle1')
cmd_vel_name = str(rospy.get_param('teleop_turtle_name'))+'/cmd_vel'



def publisher():

    # define a publisher on the /turtle1/cmd_vel topic with the imported data type on the step before;
    pub = rospy.Publisher(cmd_vel_name, Twist, queue_size=10)

    # initialize a new node with name mybot_teleop;
    rospy.init_node('mybot_teleop')

    # define a rate at which you would like the data to be published;
    #rate = rospy.Rate(10) # 10hz

    vel_msg = Twist()

    print("press 'w' to quit.")

    if not(rospy.has_param('linear_scale')) : rospy.set_param('linear_scale', 1.0)
    if not(rospy.has_param('angular_scale')): rospy.set_param('angular_scale',1.0)


    while not rospy.is_shutdown() :

        vel_msg.linear.x  = 0.
        vel_msg.angular.z = 0.

        x_param = rospy.get_param('linear_scale')
        z_param = rospy.get_param('angular_scale')

        # Get character from console
        mykey = click.getchar() # instruction bloquante => rate inutile
        if mykey in keys.keys():
            char=keys[mykey]
        
            if char == 'up'     :  vel_msg.linear.x  =  x_param
            if char == 'down'   :  vel_msg.linear.x  = -x_param
            if char == 'left'   :  vel_msg.angular.z =  z_param
            if char == 'right'  :  vel_msg.angular.z = -z_param
            if char == 'lin_acc':  rospy.set_param('linear_scale', x_param+0.05)
            if char == 'lin_dec':  rospy.set_param('linear_scale', x_param-0.05)
            if char == 'ang_acc':  rospy.set_param('angular_scale',z_param+0.1)
            if char == 'ang_dec':  rospy.set_param('angular_scale',z_param-0.1)
            if char == 'stop'   :  vel_msg.linear.x  = 0.; vel_msg.angular.z = 0.

            if char == "quit" :  break

            pub.publish(vel_msg)
        
        #rate.sleep()


if __name__ == '__main__':

    try:
        publisher()

    except rospy.ROSInterruptException:
        pass