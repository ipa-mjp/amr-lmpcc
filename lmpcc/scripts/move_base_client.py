#! /usr/bin/env python

import rospy
import sys
# Brings in the SimpleActionClient
import actionlib
import math
import tf
import geometry_msgs.msg
# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.

import move_base_msgs.msg as move

"""Reference Path"""
#x = [1.5, 3.5, 5.5, 7, 5.5, 3.5, 1.5, 0, 1.5]
#y = [0.5, 0.5, 0.5, 2, 3.5, 3.5, 3.5, 2, 0.5]
#theta = [0, 0, 0, 1.57, 3.14, 3.14, 3.14, -1.57, 0]

#global_path:
#x = [1.5, 3.5, 5.5, 7, 8, 10, 13, 11, 10.5, 9, 7, 5.5, 3.5, 1.5, 0, 1.5]
#y = [0.5, 0.5, 0.5, 2, 4, 4, 6, 7.5, 6, 4, 3.5, 3.5, 3.5, 3.5, 2, 0.5]
#theta = [0, 0, 0, 1.57, 0, 0, 1.57, 3.14, -1.57, 3.14, 3.14,  3.14, 3.14, 3.14, -1.57, 0]

# dcsc lab go out through the door
# global_path:
#x = [1.5, 3.5, 5.5, 7, 8, 10, 13, 11, 10.5, 9, 7, 5.5, 3.5, 1.5, 0, 1.5]
#y = [0.5, 0.5, 0.5, 2, 4, 4, 6, 7.5, 6, 4, 3.5, 3.5, 3.5, 3.5, 2, 0.5]
#theta = [0, 0, 0, 1.57, 0, 0, 1.57, 3.14, -1.57, 3.14, 3.14,  3.14, 3.14, 3.14, -1.57, 0]
#reference_velocity = 1.0
# Automatic doors
#global_path:
x = [7, 13, 17, 17, 14, 10, 8, 7]
y = [-0.5, -0.5, -0.5, 1.5, 1.5, 3, 3, -0.5]
theta = [0, 0, 1.57, -3.14, -3.14, -3.14, -3.14,  0]
reference_velocity = 1.0

"""ROS Variables"""
listener = tf.TransformListener()
loop = True

def move_base_client(index):
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('move_base', move.MoveBaseAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = move.MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = x[index]
    goal.target_pose.pose.position.y = y[index]
    goal.target_pose.pose.orientation.x = 0
    goal.target_pose.pose.orientation.y = 0
    goal.target_pose.pose.orientation.z = math.sin(theta[i]*0.5)
    goal.target_pose.pose.orientation.w = math.cos(theta[i]*0.5)
    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    #client.wait_for_result()

def check_if_arrived(i):

  try:
    (trans, rot) = listener.lookupTransform('map', 'base_link', rospy.Time(0))
  except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    print ("Could not get TF")
    return False

  if math.sqrt(pow(x[i]-trans[0],2)+pow(y[i]-trans[1],2)) < 1:
    return True
  else:
    return False

if __name__ == '__main__':
    i = 0

    while(i < len(x)):
      try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('move_base_client_py')
        move_base_client(i)
        arrived = False
        while not arrived:
          rospy.sleep(1)
          print("Not arrived")
          arrived = check_if_arrived(i)
      except rospy.ROSInterruptException:
        print("Failed")
        break
      i += 1

      if loop:
	      if i == len(x):
		      i = 0