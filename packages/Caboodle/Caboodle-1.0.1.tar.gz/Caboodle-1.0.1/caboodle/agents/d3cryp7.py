'''
d3cryp7 Challenge solving Agents

This module is an implementation of the Agent specification and solves a
Challenge using API calls to a d3cryp7 server. To use this Agent, create a new
instance of it and call the `solve()` function. See the unit tests for this
module for more information.
'''

from caboodle.agents.spec import Agent
from PIL import Image
import caboodle.libraries.d3cryp7 as lib
import time

class d3cryp7TextImageAgent(Agent):
	'''
	An Agent to solve image based Challenges containing text using d3cryp7

	Args:
		url (str): The URL of the d3cryp7 API
		currency (str): The currency to calculate for

	The currency must be a three letter code like USD or EUR.

	You must run a d3cryp7 server in order to use this Agent. You can find
	instructions to do so here:

	https://bitbucket.org/bkvaluemeal/d3cryp7.py
	'''

	def __init__(self, url, currency = 'USD'):
		super().__init__()

		self._last_update = 0
		self._currency = currency
		self._url = url

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

		data['result'], data['id'] = lib.recognize_image(
			self._url,
			data['image']
		)

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		if int(time.time()) > self._last_update + 60:
			self._cost = lib.get_rate(self._url, self._currency)['recognize']
			self._last_update = int(time.time())

		return self._cost

	def success(self, data):
		'''
		Performs actions for a successful Challenge

		Args:
			data (dict): The successful Challenge
		'''

		super().success(data)

		lib.success(self._url, data['id'])

	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		super().fail(data)

		lib.invalid(self._url, data['id'])

class d3cryp7TagImageGridAgent(Agent):
	'''
	An Agent to solve image grid based Challenges using d3cryp7

	Args:
		url (str): The URL of the d3cryp7 API
		currency (str): The currency to calculate for

	The currency must be a three letter code like USD or EUR.

	You must run a d3cryp7 server in order to use this Agent. You can find
	instructions to do so here:

	https://bitbucket.org/bkvaluemeal/d3cryp7.py
	'''

	def __init__(self, url, currency = 'USD'):
		super().__init__()

		self._last_update = 0
		self._currency = currency
		self._url = url

	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
		'''

		super().solve(data)

		data['result'] = ()
		results, data['ids'] = lib.tag_image_grid(
			self._url,
			data['image'],
			data['columns'],
			data['rows']
		)

		for i in range(len(results)):
			if data['tag'] in results[i]:
				data['result'] += (i,)

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		if int(time.time()) > self._last_update + 60:
			self._cost = lib.get_rate(self._url, self._currency)['tag']
			self._last_update = int(time.time())

		return self._cost

	def success(self, data):
		'''
		Performs actions for a successful Challenge

		Args:
			data (dict): The successful Challenge
		'''

		super().success(data)

		for id in data['ids']:
			lib.success(self._url, id)

	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		super().fail(data)

		for id in data['ids']:
			lib.invalid(self._url, id)
