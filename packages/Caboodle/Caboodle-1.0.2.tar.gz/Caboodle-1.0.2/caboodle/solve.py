'''
Challenge Solving Utilities

This module uses Agents to solve Challenges. Both are modular and any number of
them can be added. A Solver works by running every loaded Challenge and checking
if it returned any data. If it did, then every Solver is ran from least cost to
greatest until a result is found or a RuntimeError is raised indicating that the
Challenge could not be solved. Because of the way the Solver works, it is
imperative that every Challenge and Agent operate according to their
specifications. See the unit tests for this module for more information.
'''

from caboodle.agents.spec import Agent
from caboodle.challenges.spec import Challenge
from caboodle.web import Browser
from time import time

class Solver(object):
	'''
	Solves challenges in a Browser

	Args:
		browser (Browser): The web browser to use

	Raises:
		TypeError: The browser is not of type Browser
	'''

	def __init__(self, browser):
		if type(browser) is Browser:
			self.browser = browser
		else:
			raise TypeError('The browser must be of type Browser')

		self.challenges = []
		self.agents = []
		self.data = {}

	def solve(self):
		'''
		Solves a Challenge

		Returns:
			The ID of the Challenge

		Raises:
			RuntimeError: The Challenge could not be solved
		'''

		self.agents.sort()

		for challenge in self.challenges:
			self.browser.switch_to_default_content()

			data = challenge.get_data(self.browser)

			if data == 'solved':
				return None

			if not data:
				continue

			for agent in self.agents:
				try:
					if agent.solve(data) == 'fail':
						continue

					data['agent'] = agent
					challenge.submit_data(data)
					id = hex(int(time() * 10000000))[2:]
					self.data[id] = data

					self.browser.switch_to_default_content()

					return id
				except ValueError or RuntimeError:
					continue

		self.browser.switch_to_default_content()

		raise RuntimeError('The Challenge could not be solved')

	def add_challenge(self, challenge):
		'''
		Adds a Challenge to the list of challenge types

		Args:
			challenge (Challenge): The Challenge to add

		Raises:
			TypeError: The challenge is not of type Challenge
		'''

		if isinstance(challenge, Challenge):
			self.challenges.append(challenge)
		else:
			raise TypeError('The challenge must be of type Challenge')

	def add_agent(self, agent):
		'''
		Adds an Agent to the list of available solving agents

		Args:
			agent (Agent): The Agent to add

		Raises:
			TypeError: The agent is not of type Agent
		'''

		if isinstance(agent, Agent):
			self.agents.append(agent)
		else:
			raise TypeError('The agent must be of type Agent')

	def set_success(self, id):
		'''
		Sets a Challenge as successful and handles it appropriately before
		removing it from the list

		Args:
			id (str): The ID of the Challenge

		Raises:
			KeyError: The ID was not found
		'''

		if id:
			self.data[id]['agent'].success(self.data[id])
			del self.data[id]

	def set_fail(self, id):
		'''
		Sets a Challenge as failed and handles it appropriately before removing
		it from the list

		Args:
			id (str): The ID of the Challenge

		Raises:
			KeyError: The ID was not found
		'''

		if id:
			self.data[id]['agent'].fail(self.data[id])
			del self.data[id]
