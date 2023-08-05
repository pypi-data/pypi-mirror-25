'''
A manually defined Challenge solving Agent

This module is an implementation of the Agent specification and solves a
Challenge using an external function defined by the user. To use this Agent,
create a new instance of it with the desired solving function and call the
`solve()` function. See the unit tests for this module for more information.
'''

from caboodle.agents.spec import Agent

class ManualAgent(Agent):
	'''
	An Agent to solve Challenges with external functions

	Args:
		solve_function (function): The function to solve the Challenge
		success_function (function): The function called on success
		fail_function (function): The function called on fail

	Raises:
		TypeError: An argument is not a function

	This Agent will, by default, have a cost of zero. As a general guideline,
	the solving function should append the result to the dictionary with the
	key 'result'.

	Example:

		lambda data: data.update({'result': 42})
	'''

	def __init__(self, solve_function, success_function, fail_function):
		super().__init__()

		if callable(solve_function):
			self.solve_function = solve_function
		else:
			raise TypeError('The solve function must be a function')

		if callable(success_function):
			self.success_function = success_function
		else:
			raise TypeError('The success function must be a function')

		if callable(fail_function):
			self.fail_function = fail_function
		else:
			raise TypeError('The fail function must be a function')

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

		super().solve(data)

		return self.solve_function(data)

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

		return self.success_function(data)

	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		super().fail(data)

		return self.fail_function(data)
