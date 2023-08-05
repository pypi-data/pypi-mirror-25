'''
Solve Media CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve Solve Media CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.
'''

from caboodle.challenges.spec import Challenge
import caboodle.challenges.util as util
import time

class SolveMediaTextChallenge(Challenge):
	'''
	A Challenge for Solve Media Text CAPTCHAs

	A text CAPTCHA is the traditional type of CAPTCHA with obfuscated squiggly
	text. This Challenge will locate it if it exists and add a base64 encoded
	image of the CAPTCHA to the dictionary with the key 'image'. In addition to
	the CAPTCHA, the form to enter the result and the reload button to get a new
	CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
	respectively.
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

		try:
			data = {}

			# Get elements
			data['image'] = browser.find_element_by_xpath(
				'//img[@id="adcopy-puzzle-image-image"]'
			)
			data['form'] = browser.find_element_by_id('adcopy_response')
			data['reload'] = browser.find_element_by_id('adcopy-link-refresh')

			# Preprocess elements
			data['image'] = util.get_element_image(data['image'], browser)

			return data
		except:
			return None

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		data['form'].send_keys(data['result'])

class SolveMediaVideoChallenge(Challenge):
	'''
	A Challenge for Solve Media Video CAPTCHAs

	A video CAPTCHA is a unique type of CAPTCHA where the user must watch a
	short video before given the text to type in. This Challenge will locate the
	text if it exists and add a base64 encoded image of it to the dictionary
	with the key 'image'. In addition to the text, the form to enter the result
	and the reload button to get a new CAPTCHA are added to the dictionary with
	the keys 'form' and 'reload' respectively.
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

		try:
			data = {}

			# Play video
			browser.find_element_by_xpath('//img[@id="adcopy-poster"]').click()

			# Get elements
			while 'image' not in data:
				try:
					data['image'] = browser.find_element_by_xpath(
						'//img[@id="adcopy-ti-overlay"]'
					)
				except:
					time.sleep(1)

			data['form'] = browser.find_element_by_id('adcopy_response')
			data['reload'] = browser.find_element_by_id('adcopy-link-refresh')

			# Preprocess elements
			data['image'] = util.get_image_src(data['image'])
			data['image'] = util._process_video_captcha(data['image'])

			return data
		except:
			return None

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		data['result'] = data['result'].split(' ')[-1:][0]
		data['form'].send_keys(data['result'])

class SolveMediaEmbedChallenge(Challenge):
	'''
	A Challenge for Solve Media Embed CAPTCHAs

	An embed CAPTCHA is a type of CAPTCHA where the user is presented with an
	embedded flash object and must enter the text it contains. This Challenge
	will locate it if it exists and add a base64 encoded image of it to the
	dictionary with the key 'image'. In addition to the image, the form to enter
	the result and the reload button to get a new CAPTCHA are added to the
	dictionary with the keys 'form' and 'reload' respectively.
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

		try:
			data = {}

			# Get SWF URL
			url = browser.find_element_by_xpath(
				'//embed[@id="adcopy-puzzle-image-image"]'
			).get_attribute('src')

			# Get image
			data['image'] = util.get_image_from_swf(url, 15)

			# Get elements
			data['form'] = browser.find_element_by_id('adcopy_response')
			data['reload'] = browser.find_element_by_id('adcopy-link-refresh')

			return data
		except:
			return None

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		data['result'] = data['result'].replace(
			'Please enter the following:',
			''
		).replace(
			'Please enter:',
			''
		).strip()

		data['form'].send_keys(data['result'])

class SolveMediaRevealChallenge(Challenge):
	'''
	A Challenge for Solve Media Reveal CAPTCHAs

	A reveal CAPTCHA is a type of CAPTCHA where the user is blatantly given a
	text to type. This Challenge will locate it if it exists and add a base64
	encoded image of it to the dictionary with the key 'image'. In addition to
	the image, the form to enter the result and the reload button to get a new
	CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
	respectively.
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

		try:
			data = {}

			# Enter iframe
			iframe = browser.find_element_by_xpath(
				'//iframe[starts-with(@id, "adcopy-unique-")]'
			)
			browser.switch_to_frame(iframe)

			# Get image
			data['image'] = browser.find_element_by_id('overlay')\
				.value_of_css_property('background-image')[27:-2]

			# Return to default context
			browser.switch_to_default_content()

			# Get elements
			data['form'] = browser.find_element_by_id('adcopy_response')
			data['reload'] = browser.find_element_by_id('adcopy-link-refresh')

			# Preprocess elements
			data['image'] = util._process_reveal_captcha(data['image'])

			return data
		except:
			return None

	def submit_data(self, data):
		'''
		Submits the processed data and solves the Challenge

		Args:
			data (dict): The Challenge to submit

		Raises:
			TypeError: The data is not a dictionary
		'''

		super().submit_data(data)

		data['result'] = data['result'].replace(
			'Please Enter:',
			''
		).replace(
			'Please Enter.',
			''
		).strip()

		data['form'].send_keys(data['result'])
