#!/usr/bin/env python3

# rospy2 message_filters compatibility wrapper
# Adapts ROS 2 message_filters.Subscriber arg order to match ROS 1

import message_filters as _mf
import rospy2

class Subscriber(_mf.Subscriber):
    def __init__(self, topic, msg_type, queue_size=None, tcp_nodelay=False, **kwargs):
        super().__init__(rospy2._node, msg_type, topic)

# Re-export unchanged classes
TimeSynchronizer = _mf.TimeSynchronizer
ApproximateTimeSynchronizer = _mf.ApproximateTimeSynchronizer