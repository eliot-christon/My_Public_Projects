#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def callback( msg ):
    print('Depth =', msg.data)

if __name__ == '__main__':

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('exam_verif', anonymous=True)

    rospy.Subscriber("/depth", Float32, callback) # same topic name as the publisher

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()