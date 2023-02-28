#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For obfuscation, see https://pyob.oxyry.com/ ;-)

import rospy
import numpy as np
from std_msgs.msg import Float32
from submarinedrone.srv import depth_warning, depth_warningResponse

# ====================
# Class describing the drone
# ====================
class submarinedrone:

    def __init__(self):
        self.rate_pressure_robot=14.4   # Publication rate for pressure_remote
        self.rate_pressure_remote=1.5      # Publication rate for pressure_remote_robot
        self.freq_simu = 1/100     # Data are simulated with this frequency

        # Simulated data init
        self.pressure_robot = 0
        self.pressure_remote = 0
        self.depth = 0

        # Definition of the messages to publish
        self.message_pressure_remote=Float32()
        self.message_pressure_robot=Float32()

        # Init everything (node + service)
        rospy.init_node('submarinedrone', anonymous=False)
        self.time_init=rospy.get_time()
        rospy.Service('depth_warning', depth_warning, self.led_depth_warning)
        self.pub_pressure_remote = rospy.Publisher('/pressure_remote', Float32, queue_size=10)
        self.pub_pressure_robot= rospy.Publisher('/pressure_robot', Float32, queue_size=10)

        # Define publication rates
        rospy.Timer(rospy.Duration(1.0/self.rate_pressure_remote), self.publish_pressure_remote)
        rospy.Timer(rospy.Duration(1.0/self.rate_pressure_robot), self.publish_pressure_robot)


    # ---------------------------
    # Publisher of the pressure_remote_robot data
    # ---------------------------
    def publish_pressure_robot(self, event):
        
        
        pressure_robot_max = 16500*100
        pressure_robot_mean = 15500*100

        # Simulate pressure_remote values with a small noise
        self.pressure_robot = pressure_robot_mean + \
                      (pressure_robot_max-pressure_robot_mean)*np.cos(2*np.pi*self.freq_simu*(rospy.get_time()-self.time_init)*5) + \
                      ((np.random.random_sample(size=1)-0.5)*200)*0.5
        # Create the message and publish
        self.message_pressure_robot.data = self.pressure_robot
        self.pub_pressure_robot.publish(self.message_pressure_robot) 


    # ---------------------------
    # Publisher of the pressure_remote data
    # ---------------------------
    def publish_pressure_remote(self,event):

        pressure_remote_min = 1013*100
        pressure_remote_max = 1015*100
        pressure_remote_mean = 1013.25*100
        # Simulate depth values
        self.pressure_remote = pressure_remote_mean - \
                        (pressure_remote_max-pressure_remote_mean)*np.cos(2*np.pi*self.freq_simu*(rospy.get_time()-self.time_init))

        # Create the message and publish
        self.message_pressure_remote.data = self.pressure_remote
        self.pub_pressure_remote.publish(self.message_pressure_remote) 

    
    # ---------------------------
    # Service
    # ---------------------------
    def led_depth_warning(self, request):

        # If we want to put LED in RED
        if request.message == "WARNING":
            response = "RED"
            rospy.loginfo("LED set to RED on the remote.")
        # Else in GREEN
        elif request.message == "NORMAL":
            response = "GREEN"
            rospy.loginfo("LED set to GREEN on the remote.")
        # Else ERROR
        else:
            rospy.loginfo("Bad LED service request.")
            response = "ERROR"

        return depth_warningResponse(response)


# ====================
# Main function
# ====================
if __name__ == '__main__':
    try:
        robot = submarinedrone()    
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
