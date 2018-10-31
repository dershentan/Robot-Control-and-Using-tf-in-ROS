#!/usr/bin/env python

import roslib
import rospy
import random
import math
import tf
from random import *
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

global h_wall
h_wall = False

def callback(data):
      global h_wall
      h_wall = False
      for i in data.ranges[1:361]:
              if i <= 0.41:
                   h_wall = True

def robot1():
      rospy.init_node('robot1', anonymous=True)
      rospy.Subscriber("robot_1/base_scan", LaserScan, callback)
      robot1_pub = rospy.Publisher('robot_1/cmd_vel', Twist, queue_size=10)
      listener = tf.TransformListener()
      
      rate = rospy.Rate(10)
      listener.waitForTransform("/robot_1", "/robot_0", rospy.Time(), rospy.Duration(5.0))
      rospy.sleep(1)
      while not rospy.is_shutdown():
           twist = Twist()
           if h_wall == False:
                try:
                    now = rospy.Time.now()
                    past = now - rospy.Duration(1.0)
                    listener.waitForTransformFull("/robot_1", now,
                                      "/robot_0", past,
                                      "/world", rospy.Duration(5.0))
                    (trans, rot) = listener.lookupTransformFull("/robot_1", now,
                                      "/robot_0", past,
                                      "/world")
                except (tf.Exception, tf.LookupException, tf.ConnectivityException):
                    continue
                angular = 4 * math.atan2(trans[1], trans[0])
                linear = 2.0 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
                twist.linear.x = linear
                twist.angular.z = angular
                rdi = [-1,1]
                k = sample(rdi,1)[0]
           elif h_wall == True:
                 twist.angular.z = k*uniform(0.1,3.8);
           robot1_pub.publish(twist)
           rate.sleep()

if __name__ == '__main__':
      robot1()
