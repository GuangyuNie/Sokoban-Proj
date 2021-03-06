#!/usr/bin/env python
# encoding: utf-8

__copyright__ = "Copyright 2019, AAIR Lab, ASU"
__authors__ = ["Naman Shah", "Abhyudaya Srinet"]
__credits__ = ["Siddharth Srivastava"]
__license__ = "MIT"
__version__ = "1.0"
__maintainers__ = ["Pulkit Verma", "Abhyudaya Srinet"]
__contact__ = "aair.lab@asu.edu"
__docformat__ = 'reStructuredText'

import heapq
from problem import * 
import rospy
from std_msgs.msg import String
import numpy as np
import random

class RandomWalk:

	def __init__(self):
		self.helper = Helper()
		rospy.init_node("random_walk")
		self.publisher = rospy.Publisher("/actions", String, queue_size = 10)
		self.subscriber = rospy.Subscriber("/status", String, self.callback)
		self.init_state = self.helper.get_initial_state()
		self.current_state = self.init_state
		self.last_action = None
		rospy.Rate(1).sleep()
		print "Running"
		self.next_action()
		rospy.spin()

	def random_walk(self):
		'''
		Randomly choses an action to perform among possible actions
		'''
		while True:
			possible_next_states = self.helper.get_successor(self.current_state)
			idx = random.randint(0, len(possible_next_states.items()) - 1)
			action, state_cost = possible_next_states.items()[idx]
			next_state, cost = state_cost
			if next_state.x == -1 and next_state.y == -1:
				continue
			return next_state, action		

	def next_action(self):
		'''
		Updates current state from chosen action and publishes the action to the /actions topic
		'''
		if self.helper.is_goal_state(self.current_state):
			print "Goal Reached"
		else:
			next_state, action = self.random_walk()
			print "Executing ", action
			self.current_state = next_state
			action_str = String(data = action)
			self.publisher.publish(action_str)

	def callback(self,data):
		'''
		callback for handling status messages of turtlebot
		executes the next action when the turtlebot is ready
		'''
		if data.data == "next":
			self.next_action()


if __name__ == "__main__":
	random_walker = RandomWalk()