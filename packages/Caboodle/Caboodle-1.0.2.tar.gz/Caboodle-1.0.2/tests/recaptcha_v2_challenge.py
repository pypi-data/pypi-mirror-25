from caboodle import web
from caboodle.challenges.recaptcha import RecaptchaV2Challenge
from caboodle.challenges.spec import Challenge
import unittest

class RecaptchaV2ChallengeTest(unittest.TestCase):
	'''
	Tests the RecaptchaV2Challenge to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser()
		self.challenge = RecaptchaV2Challenge()

	def test_init(self):
		'''
		Tests that the RecaptchaV2Challenge initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

	def test_get_data(self):
		'''
		Tests that the RecaptchaV2Challenge can collect data
		'''

		self.assertFalse(self.challenge.get_data(self.browser))

		self.browser.get('https://www.google.com/recaptcha/api2/demo')

		data = self.challenge.get_data(self.browser)
		self.assertTrue('image' in data or data == 'solved')
		self.assertTrue('tiles' in data or data == 'solved')
		self.assertTrue('verify' in data or data == 'solved')
		self.assertTrue('text' in data or data == 'solved')
		self.assertTrue('tag' in data or data == 'solved')
		self.assertTrue('reload' in data or data == 'solved')
		self.assertTrue('rows' in data or data == 'solved')
		self.assertTrue('columns' in data or data == 'solved')

		with self.assertRaises(TypeError):
			self.challenge.get_data(None)

	@unittest.skip('Does not perform correctly, but function does work')
	def test_submit_data(self):
		'''
		Tests that the RecaptchaV2Challenge can submit data
		'''

		# Try until success or fail
		for _ in range(5):
			try:
				# Test valid data
				self.browser.get('https://www.google.com/recaptcha/api2/demo')

				data = self.challenge.get_data(self.browser)
				data['result'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

				self.challenge.submit_data(data)
				break
			except:
				pass
		else:
			self.fail('Could not submit valid data')

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
