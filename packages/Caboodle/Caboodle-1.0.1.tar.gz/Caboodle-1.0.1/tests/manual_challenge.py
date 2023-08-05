from caboodle import web
from caboodle.challenges.spec import Challenge
from caboodle.challenges.manual import ManualChallenge
import unittest

class ManualChallengeTest(unittest.TestCase):
	'''
	Tests the ManualChallenge to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser()
		self.challenge = ManualChallenge(
			lambda browser: {'text': 'What is the answer to the question?'},
			lambda data: data['result']
		)

	def test_init(self):
		'''
		Tests that the ManualChallenge initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

		with self.assertRaises(TypeError):
			ManualChallenge(
				None,
				lambda data: data['result']
			)

		with self.assertRaises(TypeError):
			ManualChallenge(
				lambda browser: {'text': 'What is the answer to the question?'},
				None
			)

	def test_get_data(self):
		'''
		Tests that the ManualChallenge can collect data
		'''

		data = self.challenge.get_data(self.browser)
		self.assertTrue(data['text'])

		with self.assertRaises(TypeError):
			self.challenge.get_data(None)

	def test_submit_data(self):
		'''
		Tests that the ManualChallenge can submit data
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
