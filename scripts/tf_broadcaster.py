#!/usr/bin/env python

import rospy
import tf
from nav_msgs.msg import Odometry

def handle_odom(msg, robotname):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z),
                     (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w),
                     rospy.Time.now(),
                     robotname,
                     "world")

if __name__ == '__main__':
    rospy.init_node('tf_broadcaster')
    robotname = rospy.get_param('~robot')
    rospy.Subscriber('/%s/odom' % robotname,
                     Odometry,
                     handle_odom,
                     robotname)
    rospy.spin()
