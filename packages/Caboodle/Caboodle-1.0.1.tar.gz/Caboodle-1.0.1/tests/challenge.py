from caboodle import web
from caboodle.challenges.spec import Challenge
import unittest

class GoodChallenge(Challenge):
	'''
	A complete child of the Challenge specification
	'''

	def __init__(self):
		super().__init__()

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

		return {'text': 'What is the answer to the question?'}

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		return data['result']

class BadChallenge(Challenge):
	'''
	An incomplete child of the Challenge specification
	'''

	def __init__(self):
		super().__init__()

class ChallengeTest(unittest.TestCase):
	'''
	Tests the Challenge specification to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser()
		self.challenge = GoodChallenge()

	def test_abstraction(self):
		'''
		Tests that an incomplete child of the Challenge specification will
		raise a TypeError
		'''

		with self.assertRaises(TypeError):
			BadChallenge()

	def test_init(self):
		'''
		Tests that the Challenge specification initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

	def test_get_data(self):
		'''
		Tests that the Challenge specification can collect data
		'''

		data = self.challenge.get_data(self.browser)
		self.assertTrue(data['text'])

		with self.assertRaises(TypeError):
			self.challenge.get_data(None)

	def test_submit_data(self):
		'''
		Tests that the Challenge specification can submit data
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 42
		}
		self.assertEqual(self.challenge.submit_data(data), 42)

		with self.assertRaises(TypeError):
			self.challenge.submit_data(None)

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
