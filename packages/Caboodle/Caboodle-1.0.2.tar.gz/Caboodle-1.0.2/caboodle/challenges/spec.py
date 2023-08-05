'''
Specifications for Challenge objects

This module defines abstract classes with compounding levels of functionality.
Every Challenge should have a `get_data()` and `submit_data()` function. These
specifications can not be instantiated and can only be used by a subclass that
implements all of the required functions. Be sure, however, to explicitly call
the `super()` function from each subclass and from each defined function in
that subclass to gain the functionality of it's parent. See the unit tests for
this module for more information.
'''

from abc import ABCMeta, abstractmethod
from caboodle.web import Browser

class Challenge(object, metaclass = ABCMeta):
	'''
	An object that represents a challenge

	A Challenge collects data and packages it into a dictionary to be processed.
	Once that data has been processed, it can then submit the result in the
	required way. As a general guideline, processed data should contain a key
	named 'result' and so a Challenge may depend on that when submitting. In
	addition, collected data should be organized logically. For example, if the
	Challenge requires an image to be solved, it should be base64 encoded and
	appended to the dictionary with the key 'image'.
	'''

	def __init__(self):
		pass

	@abstractmethod
	def get_data(self, browser):
		'''
		Collects data needed to solve the Challenge

		Args:
			browser (Browser): The web browser to use

		Returns:
			A dictionary of collected data

		Raises:
			TypeError: The browser is not of type Browser
		'''

		if type(browser) is not Browser:
			raise TypeError('The browser must be of type Browser')

	@abstractmethod
	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		if type(data) is not dict:
			raise TypeError('The data must be a dictionary')
