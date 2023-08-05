from caboodle import web
import caboodle.challenges.util as util
import os
import unittest

DEBIAN = None
SM_REVEAL0 = None
SM_REVEAL1 = None
SM_VIDEO0 = None
SM_VIDEO1 = None
TACO = None
WIKIPEDIA = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'debian' in files:
		DEBIAN = os.path.join(root, 'debian')
		DEBIAN = open(DEBIAN, 'rb').read()

	if 'sm_reveal0' in files:
		SM_REVEAL0 = os.path.join(root, 'sm_reveal0')
		SM_REVEAL0 = open(SM_REVEAL0, 'rb').read()

	if 'sm_reveal1' in files:
		SM_REVEAL1 = os.path.join(root, 'sm_reveal1')
		SM_REVEAL1 = open(SM_REVEAL1, 'rb').read()

	if 'sm_video0' in files:
		SM_VIDEO0 = os.path.join(root, 'sm_video0')
		SM_VIDEO0 = open(SM_VIDEO0, 'rb').read()

	if 'sm_video1' in files:
		SM_VIDEO1 = os.path.join(root, 'sm_video1')
		SM_VIDEO1 = open(SM_VIDEO1, 'rb').read()

	if 'taco_tuesday' in files:
		TACO = os.path.join(root, 'taco_tuesday')
		TACO = open(TACO, 'rb').read()

	if 'wikipedia' in files:
		WIKIPEDIA = os.path.join(root, 'wikipedia')
		WIKIPEDIA = open(WIKIPEDIA, 'rb').read()

class UtilTest(unittest.TestCase):
	'''
	Tests the Challenge utility functions to verify they work correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Browser to use
		'''

		self.browser = web.Browser()

	def test_get_element_image(self):
		'''
		Tests that the function returns the correct image
		'''

		if WIKIPEDIA:
			self.browser.get('https://www.wikipedia.org')

			image = self.browser.find_element_by_tag_name('img')
			image = util.get_element_image(image, self.browser)

			self.assertEqual(image, WIKIPEDIA)
		else:
			self.fail('Could not locate data file')

	def test_get_image_src(self):
		'''
		Tests that the function returns the correct image
		'''

		if DEBIAN:
			self.browser.get('https://www.debian.org')

			image = self.browser.find_element_by_tag_name('img')
			image = util.get_image_src(image)

			self.assertEqual(image, DEBIAN)
		else:
			self.fail('Could not locate data file')

	@unittest.skip('SWF is no longer rendered')
	def test_get_image_from_swf(self):
		'''
		Tests that the function returns the correct image
		'''

		if TACO:
			image = util.get_image_from_swf(
				'https://api-secure.solvemedia.com/acmedia/g/L'\
				'/gLz89YKzrdedeMOs/S/Sr.89ZNCrdedf8Px.swf',
				15
			)

			self.assertEqual(image, TACO)
		else:
			self.fail('Could not locate data file')

	def test_process_video_captcha(self):
		'''
		Tests that the function returns the correct image
		'''

		if SM_VIDEO0 and SM_VIDEO1:
			image = util._process_video_captcha(SM_VIDEO0)

			self.assertEqual(image, SM_VIDEO1)
		else:
			self.fail('Could not locate data file')

	def test_process_reveal_captcha(self):
		'''
		Tests that the function returns the correct image
		'''

		if SM_REVEAL0 and SM_REVEAL1:
			image = util._process_reveal_captcha(SM_REVEAL0)

			self.assertEqual(image, SM_REVEAL1)
		else:
			self.fail('Could not locate data file')

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
