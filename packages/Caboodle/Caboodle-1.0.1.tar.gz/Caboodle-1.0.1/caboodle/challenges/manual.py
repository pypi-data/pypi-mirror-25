'''
A manually defined Challenge

This module is an implementation of the Challenge specification and collects
data using an external function defined by the user. To use this Challenge,
create a new instance of it with the desired functions and call the `get_data()`
function. Then, process the data using an Agent and submit it by calling the
`submit_data()` function. See the unit tests for this module for more
information.
'''

from caboodle.challenges.spec import Challenge

class ManualChallenge(Challenge):
	'''
	A Challenge that uses external functions

	Args:
		get_function (function): The function to collect data
		submit_function (function): The function to submit data

	Raises:
		TypeError: The arguments are not functions

	As a general guideline, processed data should contain a key named 'result'
	and so the `submit_function` may depend on that when submitting. In
	addition, collected data should be organized logically. For example, if the
	Challenge requires an image to be solved, it should be base64 encoded and
	appended to the dictionary with the key 'image'.
	'''

	def __init__(self, get_function, submit_function):
		super().__init__()

		if callable(get_function):
			self.get_function = get_function
		else:
			raise TypeError('The get function must be a function')

		if callable(submit_function):
			self.submit_function = submit_function
		else:
			raise TypeError('The submit function must be a function')

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

		super().get_data(browser)

		return self.get_function(browser)

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		return self.submit_function(data)
