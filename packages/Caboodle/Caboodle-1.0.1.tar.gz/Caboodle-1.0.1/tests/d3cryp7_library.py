from unittest import mock
import caboodle.libraries.d3cryp7 as lib
import os
import unittest

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

def flip_flop_get(*args, **kwarg):
	'''
	Replaces the `requests.get()` function by flipping the status code from 404
	to 200 to test the less complex functions `get_rate()`
	'''

	if URL in args[0]:
		if FLIP_FLOP():
			return MockResponse(D3CRYP7_RESPONSE, 200)
		else:
			return MockResponse('', 404)
	elif 'fixer' in args[0]:
		if FLIP_FLOP():
			return MockResponse(FIXER_RESPONSE, 200)
		else:
			return MockResponse('', 404)
	else:
		return MockResponse(None, 404)

URL = 'http://localhost'
HELLO_WORLD = None
CAR = None
TRUCKS = None
BB33 = (
	(  0,   0, 100, 100), (100,   0, 200, 100), (200,   0, 300, 100),
	(  0, 100, 100, 200), (100, 100, 200, 200), (200, 100, 300, 200),
	(  0, 200, 100, 300), (100, 200, 200, 300), (200, 200, 300, 300)
)
BB42 = (
	(  0,   0, 150,  75), (150,   0, 300,  75),
	(  0,  75, 150, 150), (150,  75, 300, 150),
	(  0, 150, 150, 225), (150, 150, 300, 225),
	(  0, 225, 150, 300), (150, 225, 300, 300)
)
FLIP_FLOP = FlipFlop()
D3CRYP7_RESPONSE = None
FIXER_RESPONSE = None

# Locate data files and read them
for root, dirs, files in os.walk(os.getcwd()):
	if 'hello_world' in files:
		HELLO_WORLD = os.path.join(root, 'hello_world')
		HELLO_WORLD = open(HELLO_WORLD, 'rb').read()

	if 'car' in files:
		CAR = os.path.join(root, 'car')
		CAR = open(CAR, 'rb').read()

	if 'commercial_trucks' in files:
		TRUCKS = os.path.join(root, 'commercial_trucks')
		TRUCKS = open(TRUCKS, 'rb').read()

	if 'd3cryp7_response' in files:
		D3CRYP7_RESPONSE = os.path.join(root, 'd3cryp7_response')
		D3CRYP7_RESPONSE = open(D3CRYP7_RESPONSE, 'r').read()
		D3CRYP7_RESPONSE = D3CRYP7_RESPONSE.replace('\n', '\r\n')

	if 'fixer_response' in files:
		FIXER_RESPONSE = os.path.join(root, 'fixer_response')
		FIXER_RESPONSE = open(FIXER_RESPONSE, 'r').read()

class d3cryp7LibraryTest(unittest.TestCase):
	'''
	Tests the d3cryp7 library to verify that it works correctly
	'''

	def test_recognize_image(self):
		'''
		Tests that the function correctly posts an image and returns the result
		'''

		if HELLO_WORLD:
			self.assertEqual(
				lib.recognize_image(URL, HELLO_WORLD)[0],
				'Hello\nWorld'
			)

			with self.assertRaises(RuntimeError):
				lib.recognize_image(URL, None)

			with self.assertRaises(RuntimeError):
				lib.recognize_image('http://google.com', None)
		else:
			self.fail('Could not locate data file')

	def test_tag_image(self):
		'''
		Tests that the function correctly posts an image and returns the result
		'''

		if CAR:
			self.assertIn(
				'car',
				lib.tag_image(URL, CAR)[0]
			)

			with self.assertRaises(RuntimeError):
				lib.tag_image(URL, None)

			with self.assertRaises(RuntimeError):
				lib.tag_image('http://google.com', None)
		else:
			self.fail('Could not locate data file')

	def test_tag_image_grid(self):
		'''
		Tests that the function correctly posts an image and returns the result
		'''

		if TRUCKS:
			for result in lib.tag_image_grid(URL, TRUCKS, 3, 3):
				self.assertEqual(type(result), tuple)

			with self.assertRaises(RuntimeError):
				lib.tag_image_grid(URL, None, 1, 1)

			with self.assertRaises(RuntimeError):
				lib.tag_image_grid('http://google.com', None, 1, 1)
		else:
			self.fail('Could not locate data file')

	def test_generate_bbs(self):
		'''
		Tests that the function correctly generates bounding boxes
		'''

		self.assertEqual(lib.generate_bbs(300, 300, 3, 3), BB33)
		self.assertEqual(lib.generate_bbs(300, 300, 2, 4), BB42)

	@mock.patch(
		'caboodle.libraries.d3cryp7.requests.get',
		side_effect = flip_flop_get
	)
	def test_get_cost(self, mock_get):
		'''
		Tests that the function returns the correct result
		'''

		if D3CRYP7_RESPONSE and FIXER_RESPONSE:
			data = lib.get_rate(URL, 'EUR')
			self.assertIn('recognize', data)
			self.assertIn('tag', data)

			FLIP_FLOP.set(True)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
