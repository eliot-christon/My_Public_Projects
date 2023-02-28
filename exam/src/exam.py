#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float32

from submarinedrone.srv import depth_warning


class MyNode :
    """The class for this exam_node"""

    def __init__( self ) :

        self.preRob = 0. # pressure_robot value
        self.preRem = 0. # pressure_remote value

        self.depth = 1.  # depth value

        self.preRob_resp = False # new value pending
        self.preRem_resp = False # new value pending

        # getting threshold param in an attribute
        if rospy.has_param('~threshold') : # if the param exits => get it
            self.threshold = rospy.get_param('~threshold')
        else : self.threshold = 150        # else => default value

        # ARGS : name of the topic, type of msg delivered, callback_function called when receiving a new msg
        rospy.Subscriber("/pressure_robot", Float32, self.callback_rob) # same topic name as the publisher
        rospy.Subscriber("/pressure_remote"   , Float32, self.callback_rem) # same topic name as the publisher

        # creating a publisher on the '/depth' topic
        self.pub_depth = rospy.Publisher('/depth', Float32, queue_size=10)

        # waiting for the service to be ready
        rospy.wait_for_service('depth_warning')
        # creating a handler of "depth_warning" service
        self.warning = rospy.ServiceProxy('depth_warning',depth_warning)

        # let's now enter the main loop
        self.main_loop()


    def main_loop( self ) :
        """publish depth value and request on depth_warning service"""

        # init local variables
        countInSec = 0.        # the count in seconds
        warn = False           # current warning state
        self.warning("NORMAL") # init the service to "NORMAL"

        # let's define a rate
        hz = 10 # at how many Hertz should it be ?
        rate = rospy.Rate(hz)

        while not rospy.is_shutdown(): # main loop, until the node is shutdown

            countInSec += 1/hz  # incrementing the count from the rate period
            
            self.update_depth() # updating the new depth value

            if (self.depth > self.threshold) and (countInSec > 5) and not(warn) :
            # IF the submarine is too low for 5 seconds and the warning isn't activated yet
                resp = self.warning("WARNING") # call the service with "WARNING"
                print(resp) # print the response to the screen (facultative)
                warn = True # current warning state is now True

            elif self.depth < self.threshold and warn:
            # ELSE IF the submarine is not too low and the warning is activated
                resp = self.warning("NORMAL") # call the service with "NORMAL"
                print(resp)  # print the response to the screen (facultative)
                warn = False # current warning state is now False
            
            if self.depth < self.threshold :
            # IF the submarine isn't too low
                countInSec = 0. # restart the count

            self.pub_depth.publish(self.depth) # publishing the new altitude value in the corresponding topic
            rate.sleep()                       # waiting for the rate


    def update_depth( self, rho=1030, g=9.80665) :
        """compute a new depth value"""
        self.depth = (self.preRob - self.preRem) / (rho * g) # the attribute is given the new depth value


    def callback_rob( self, msg ) : # takes the topic content as input
        """called each time the subscriber receive a new pressure robot value"""
        self.preRob = msg.data  # new temperature value
        self.preRob_resp = True # put the pressure robot response attribute to True
        self.aff_msg()       # call the aff_msg() function


    def callback_rem( self, msg ) : # takes the topic content as input
        """called each time the subscriber receive a new pressure remote value"""
        self.preRem = msg.data  # new temperature value
        self.preRem_resp = True # put the pressure remote response attribute to True
        self.aff_msg()       # call the aff_msg() function


    def aff_msg( self, wait_for_both_topics = True ) :
        """prints the robot and remote pressure
        if wait_for_both_topics = True it will wait for both temperature and pressure to be updated"""
        if (self.preRob_resp and self.preRem_resp) or not(wait_for_both_topics) :
            print(f"Pressure \t Robot : {self.preRob} \tRemote : {self.preRem}")
            self.preRob_resp = False
            self.preRem_resp = False





if __name__ == '__main__':

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('exam', anonymous=True)

    # creating a MyNode object, (2*subscriber + 1*publisher + 1*service)
    MyNode()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
