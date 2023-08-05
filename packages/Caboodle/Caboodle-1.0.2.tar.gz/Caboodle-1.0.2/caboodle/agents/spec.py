'''
Specifications for Challenge solving agents

This module defines abstract classes with compounding levels of functionality.
Every Agent should have a `solve()` and `get_cost()` function and, by default,
will initialize the cost of the Agent to zero. These specifications can not be
instantiated and can only be used by a subclass that implements all of the
required functions. Be sure, however, to explicitly call the `super()` function
from each subclass and from each defined function in that subclass to gain the
functionality of it's parent. See the unit tests for this module for more
information.
'''

from abc import ABCMeta, abstractmethod

class Agent(object, metaclass = ABCMeta):
	'''
	An agent to solve Challenges

	An Agent processes data from a Challenge in the form of a dictionary to
	produce a result. This result is added to the dictionary if and when it
	succeeds. As a general guideline, the result should be appended to the
	dictionary with the key 'result'.
	'''

	def __init__(self):
		self._cost = 0.0

	@abstractmethod
	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
			ValueError: The Challenge does not contain the required data
			RuntimeError: The Challenge could not be solved
		'''

		if type(data) is not dict:
			raise TypeError('The data must be a dictionary')

	@abstractmethod
	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		return self._cost

	@abstractmethod
	def success(self, data):
		'''
		Performs actions for a successful Challenge

		Args:
			data (dict): The successful Challenge
		'''

		pass

	@abstractmethod
	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		pass

	def __lt__(self, other):
		'''
		Compares the cost of this agent to another

		Args:
			other (solver): The other agent to compare

		Returns:
			True if the cost of this agent is less than another

		Raises:
			TypeError: The other agent is not of type Agent
		'''

		if isinstance(other, Agent):
			return self.get_cost() < other.get_cost()
		else:
			raise TypeError('The other agent must be of type Agent')
