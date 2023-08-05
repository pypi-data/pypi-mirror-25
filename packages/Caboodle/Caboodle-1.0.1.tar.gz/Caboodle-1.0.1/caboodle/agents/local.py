'''
A local Challenge solving Agent

This module is an implementation of the Agent specification and solves a
Challenge using the `input()` function. To use this Agent, create a new instance
of it and call the `solve()` function. See the unit tests for this module for
more information.
'''

from caboodle.agents.spec import Agent

class LocalAgent(Agent):
	'''
	An Agent to solve Challenges with input from the user

	This Agent uses the `input()` function and thus will block the execution of
	your application until it receives input. The result is appended to the
	dictionary with the key 'result' as per the guidelines. Because this Agent
	relies on user input, it has a cost of zero.
	'''

	def __init__(self):
		super().__init__()

	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
		'''

		super().solve(data)

		data['result'] = input('Please solve the challenge: ')

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		return self._cost

	def success(self, data):
		'''
		Performs actions for a successful Challenge

		Args:
			data (dict): The successful Challenge
		'''

		super().success(data)

	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		super().fail(data)
