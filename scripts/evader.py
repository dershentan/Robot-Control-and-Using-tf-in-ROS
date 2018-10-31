#!/usr/bin/env python

import rospy
import random
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

def robot0():
      rospy.init_node('robot0', anonymous=True)
      rospy.Subscriber("base_scan", LaserScan, callback)
      robot0_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
      
      rate = rospy.Rate(100)
      while not rospy.is_shutdown():
           twist = Twist()
           if h_wall == False:
                twist.linear.x = 2.0;
                rdi = [-1,1]
                k = sample(rdi,1)[0]
           elif h_wall == True:
                 twist.angular.z = k*uniform(0.1,3.8);
           robot0_pub.publish(twist)
           rate.sleep()

if __name__ == '__main__':
      robot0()
