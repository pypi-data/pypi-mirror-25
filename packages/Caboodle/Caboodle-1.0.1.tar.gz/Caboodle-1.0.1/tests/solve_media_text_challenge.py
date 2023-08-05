from caboodle import web
from caboodle.challenges.solve_media import SolveMediaTextChallenge
from caboodle.challenges.spec import Challenge
import os
import time
import unittest

HTML = None

# Locate html file
for root, dirs, files in os.walk(os.getcwd()):
	if 'solve_media.html' in files:
		HTML = 'file://' + os.path.join(root, 'solve_media.html')

class SolveMediaTextChallengeTest(unittest.TestCase):
	'''
	Tests the SolveMediaTextChallenge to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Challenge to test
		'''

		self.browser = web.Browser()
		self.challenge = SolveMediaTextChallenge()

	def test_init(self):
		'''
		Tests that the SolveMediaTextChallenge initializes correctly
		'''

		self.assertIsInstance(self.challenge, Challenge)

	def test_get_data(self):
		'''
		Tests that the SolveMediaTextChallenge can collect data
		'''

		if HTML:
			self.assertFalse(self.challenge.get_data(self.browser))

			self.browser.get(HTML)

			# Wait for page to load
			while True:
				try:
					self.browser.find_element_by_id('show').click()
					break
				except:
					time.sleep(1)

			# Wait for CAPTCHA to load
			while True:
				try:
					self.browser.find_element_by_id('adcopy-puzzle-image-image')
					self.browser.find_element_by_id('adcopy_response')
					self.browser.find_element_by_id('adcopy-link-refresh')
					break
				except:
					time.sleep(1)

			data = self.challenge.get_data(self.browser)
			self.assertTrue(data)
			self.assertTrue(data['image'])
			self.assertTrue(data['form'])
			self.assertTrue(data['reload'])

			with self.assertRaises(TypeError):
				self.challenge.get_data(None)
		else:
			self.fail('Could not locate html file')

	def test_submit_data(self):
		'''
		Tests that the SolveMediaTextChallenge can submit data
		'''

		if HTML:
			self.browser.get(HTML)

			# Wait for page to load
			while True:
				try:
					self.browser.find_element_by_id('show').click()
					break
				except:
					time.sleep(1)

			# Wait for CAPTCHA to load
			while True:
				try:
					self.browser.find_element_by_id('adcopy-puzzle-image-image')
					self.browser.find_element_by_id('adcopy_response')
					self.browser.find_element_by_id('adcopy-link-refresh')
					break
				except:
					time.sleep(1)

			data = self.challenge.get_data(self.browser)
			print(data)
			data['result'] = '42'

			self.challenge.submit_data(data)

			self.assertEqual(data['form'].get_attribute('value'), '42')
		else:
			self.fail('Could not locate html file')

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
