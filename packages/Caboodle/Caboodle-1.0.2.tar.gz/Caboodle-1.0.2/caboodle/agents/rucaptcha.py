'''
ruCaptcha Challenge solving Agents

This module is an implementation of the Agent specification and solves a
Challenge using the paid online service ruCaptcha. To use these Agents, create a
new instance of one and call the `solve()` function. See the documentation for
each Agent and their respective unit tests for more information.
'''

from caboodle.agents.spec import Agent
import caboodle.libraries.rucaptcha as lib
import time

class RucaptchaImageAgent(Agent):
	'''
	An Agent to solve image based Challenges using ruCaptcha

	Args:
		key (str): The API key to use
		currency (str): The currency to calculate for

	The currency must be a three letter code like USD or EUR.
	'''

	def __init__(self, key, currency = 'USD'):
		super().__init__()

		self._last_update = 0
		self._key = key
		self._currency = currency
		self.get_cost()

	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
		'''

		super().solve(data)

		# Stop if challenge is image grid
		if 'columns' in data or 'rows' in data:
			return 'fail'

		data['id'] = lib.post_image(self._key, data['image'])
		data['result'] = lib.get(self._key, data['id'])

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		if int(time.time()) > self._last_update + 60:
			self._cost = lib.get_rate(self._currency)
			self._last_update = int(time.time())

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

		lib.invalid(self._key, data['id'])

class RucaptchaImageGridAgent(Agent):
	'''
	An Agent to solve image grid based Challenges using ruCaptcha

	Args:
		key (str): The API key to use
		currency (str): The currency to calculate for

	The currency must be a three letter code like USD or EUR.
	'''

	def __init__(self, key, currency = 'USD'):
		super().__init__()

		self._last_update = 0
		self._key = key
		self._currency = currency
		self.get_cost()

	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
		'''

		super().solve(data)

		data['id'] = lib.post_image_grid(
			self._key,
			data['image'],
			data['text'],
			data['rows'],
			data['columns']
		)
		data['result'] = lib.get(self._key, data['id'])
		data['result'] = data['result'].split(':')[1].split('/')
		data['result'] = tuple([int(i) - 1 for i in data['result']])

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		if int(time.time()) > self._last_update + 60:
			self._cost = lib.get_rate(self._currency, 0.07)
			self._last_update = int(time.time())

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

		lib.invalid(self._key, data['id'])
