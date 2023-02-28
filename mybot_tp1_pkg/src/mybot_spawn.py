#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from turtlesim.srv import Spawn, SpawnRequest


if __name__ == '__main__':
    try:
        # initialise a new ROS node with name mybot_color;
        rospy.init_node('mybot_spawn')

        rospy.wait_for_service('/spawn')
        spawn_handle = rospy.ServiceProxy('/spawn',Spawn)

        spawn_request = SpawnRequest()

        spawn_request.x = 5.4
        spawn_request.y = 5.4
        spawn_request.theta = 0.5
        spawn_request.name = str(rospy.get_param('teleop_turtle_name'))

        spawn_handle(spawn_request)

        # And then ... wait for the node to be terminated
        # rospy.spin() # or not

    except rospy.ROSInterruptException:
        pass