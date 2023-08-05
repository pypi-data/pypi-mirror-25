from io import BytesIO
from PIL import Image
from unittest import mock
import base64
import caboodle.libraries.rucaptcha as lib
import os
import unittest

class Counter(object):
	'''
	Creates an integer counter that increments the value every time it is used
	'''

	def __init__(self):
		self.state = 0

	def __call__(self):
		self.state += 1
		return self.state

	def set(self, state):
		'''
		Sets the state of the Counter

		Args:
			state (int): The state of the Counter
		'''

		self.state = state

class FlipFlop(object):
	'''
	Creates a boolean that changes value every time it is used
	'''

	def __init__(self):
		self.state = True

	def __call__(self):
		self.state = not self.state
		return self.state

	def set(self, state):
		'''
		Sets the state of the FlipFlop

		Args:
			state (bool): The state of the FlipFlop
		'''

		self.state = state

class MockResponse(object):
	'''
	Simulates a result from the requests module

	Args:
		text (str): The content returned
		status_code (int): The HTTP status code
	'''

	def __init__(self, text, status_code):
		self.status_code = status_code
		self.ok = status_code == 200
		self.text = text

def counter_post(*args, **kwags):
	'''
	Replaces the `requests.post()` function by stepping through a series of
	states to test the more complex `post()` function
	'''

	state = COUNTER()
	if state == 1:
		return MockResponse('', 404)
	elif state == 2:
		return MockResponse('ERROR_NO_SLOT_AVAILABLE', 200)
	elif state == 3:
		return MockResponse('THIS_SHOULD|NEVER_HAPPEN', 200)
	elif state == 4:
		return MockResponse('OK|42', 200)
	else:
		return MockResponse(None, 404)

def counter_get_image(*args, **kwags):
	'''
	Replaces the `requests.get()` function by stepping through a series of
	states to test the more complex `get()` function
	'''

	state = COUNTER()
	if state == 1:
		return MockResponse('', 404)
	elif state == 2:
		return MockResponse('ERROR_KEY_DOES_NOT_EXIST', 200)
	elif state == 3:
		return MockResponse('CAPCHA_NOT_READY', 200)
	elif state == 4:
		return MockResponse('OK|Python', 200)
	else:
		return MockResponse(None, 404)

def counter_get_image_grid(*args, **kwags):
	'''
	Replaces the `requests.get()` function by stepping through a series of
	states to test the more complex `get()` function
	'''

	state = COUNTER()
	if state == 1:
		return MockResponse('', 404)
	elif state == 2:
		return MockResponse('ERROR_KEY_DOES_NOT_EXIST', 200)
	elif state == 3:
		return MockResponse('CAPCHA_NOT_READY', 200)
	elif state == 4:
		return MockResponse('OK|click:1/4/5', 200)
	else:
		return MockResponse(None, 404)

def flip_flop_get(*args, **kwarg):
	'''
	Replaces the `requests.get()` function by flipping the status code from 404
	to 200 to test the less complex functions `invalid()` and `get_rate()`
	'''

	if 'rucaptcha' in args[0]:
		if FLIP_FLOP():
			if 'params' in kwarg:
				return MockResponse('', 200)
			else:
				return MockResponse(RUCAPTCHA_RESPONSE, 200)
		else:
			return MockResponse('', 404)
	elif 'fixer' in args[0]:
		if FLIP_FLOP():
			return MockResponse(FIXER_RESPONSE, 200)
		else:
			return MockResponse('', 404)
	else:
		return MockResponse(None, 404)

PYTHON = None
TRUCKS = None
RUCAPTCHA_RESPONSE = None
FIXER_RESPONSE = None
FLIP_FLOP = FlipFlop()
COUNTER = Counter()

# Locate data files and read them
for root, dirs, files in os.walk(os.getcwd()):
	if 'python' in files:
		PYTHON = os.path.join(root, 'python')
		PYTHON = open(PYTHON, 'rb').read()

	if 'commercial_trucks' in files:
		TRUCKS = os.path.join(root, 'commercial_trucks')
		TRUCKS = open(TRUCKS, 'rb').read()

	if 'rucaptcha_response' in files:
		RUCAPTCHA_RESPONSE = os.path.join(root, 'rucaptcha_response')
		RUCAPTCHA_RESPONSE = open(RUCAPTCHA_RESPONSE, 'r').read()
		RUCAPTCHA_RESPONSE = RUCAPTCHA_RESPONSE.replace('\n', '\r\n')

	if 'fixer_response' in files:
		FIXER_RESPONSE = os.path.join(root, 'fixer_response')
		FIXER_RESPONSE = open(FIXER_RESPONSE, 'r').read()

class RucaptchaLibraryTest(unittest.TestCase):
	'''
	Tests the ruCaptcha library to verify that it works correctly
	'''

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.post',
		side_effect = counter_post
	)
	def test_post_image(self, mock_post):
		'''
		Tests that the function correctly posts an image and returns the ID
		'''

		if PYTHON:
			with self.assertRaises(RuntimeError):
				lib.post_image('API KEY', PYTHON)

			with self.assertRaises(RuntimeError):
				lib.post_image('API KEY', PYTHON)

			with self.assertRaises(RuntimeError):
				lib.post_image('API KEY', PYTHON)

			self.assertEqual(lib.post_image('API KEY', PYTHON), '42')
			COUNTER.set(0)
		else:
			self.fail('Could not locate data file')

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.post',
		side_effect = counter_post
	)
	def test_post_image_grid(self, mock_post):
		'''
		Tests that the function correctly posts an image grid and returns the ID
		'''

		if TRUCKS:
			with self.assertRaises(RuntimeError):
				lib.post_image_grid(
					'API KEY',
					TRUCKS,
					'Select all images with commercial trucks',
					3,
					3
				)

			with self.assertRaises(RuntimeError):
				lib.post_image_grid(
					'API KEY',
					TRUCKS,
					'Select all images with commercial trucks',
					3,
					3
				)

			with self.assertRaises(RuntimeError):
				lib.post_image_grid(
					'API KEY',
					TRUCKS,
					'Select all images with commercial trucks',
					3,
					3
				)

			self.assertEqual(
				lib.post_image_grid(
					'API KEY',
					TRUCKS,
					'Select all images with commercial trucks',
					3,
					3
				),
				'42'
			)
			COUNTER.set(0)
		else:
			self.fail('Could not locate data file')

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.get',
		side_effect = counter_get_image
	)
	def test_get_image(self, mock_get):
		'''
		Tests that the function returns the result of the posted image
		'''

		with self.assertRaises(RuntimeError):
			lib.get('API KEY', 42)

		with self.assertRaises(RuntimeError):
			lib.get('API KEY', 42)

		self.assertEqual(lib.get('API KEY', 42), 'Python')
		COUNTER.set(0)

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.get',
		side_effect = counter_get_image_grid
	)
	def test_get_image_grid(self, mock_get):
		'''
		Tests that the function returns the result of the posted image grid
		'''

		with self.assertRaises(RuntimeError):
			lib.get('API KEY', 42)

		with self.assertRaises(RuntimeError):
			lib.get('API KEY', 42)

		self.assertEqual(lib.get('API KEY', 42), 'click:1/4/5')
		COUNTER.set(0)

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.get',
		side_effect = flip_flop_get
	)
	def test_invalid(self, mock_get):
		'''
		Tests that the function works correctly and does not raise any
		exceptions
		'''

		lib.invalid('API KEY', 42)
		FLIP_FLOP.set(True)

	@mock.patch(
		'caboodle.libraries.rucaptcha.requests.get',
		side_effect = flip_flop_get
	)
	def test_get_rate(self, mock_get):
		'''
		Tests that the function returns the correct result
		'''

		if RUCAPTCHA_RESPONSE and FIXER_RESPONSE:
			self.assertEqual(int(lib.get_rate('USD') * 10000000000), 7448445)
			FLIP_FLOP.set(True)
		else:
			self.fail('Could not locate data file')

	def test_scale_image(self):
		'''
		Tests that the function can scale an image while maintaining the aspect
		ratio to within 0.1% of the original
		'''

		ratio = 290 / 82
		ratio_plus = ratio + ratio * 0.001
		ratio_minus = ratio - ratio * 0.001

		if PYTHON:
			image = lib.scale_image(PYTHON)
			image = BytesIO(base64.b64decode(image))
			image = Image.open(image)

			w, h = image.size
			actual = w / h

			if actual < ratio_minus and actual > ratio_plus:
				difference = actual - ratio
				average = (actual + ratio) / 2

				# Absolute value
				if difference < 0.0:
					difference -= 2 * difference

				percent_diff = (difference / average) * 100

				self.fail('The aspect ratio was %f% different' % percent_diff)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
