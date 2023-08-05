from caboodle.agents.rucaptcha import RucaptchaImageAgent
from unittest import mock
import os
import unittest

PYTHON = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'python' in files:
		PYTHON = os.path.join(root, 'python')
		PYTHON = open(PYTHON, 'rb').read()

class RucaptchaImageAgentTest(unittest.TestCase):
	'''
	Tests the RucaptchaImageAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a RucaptchaImageAgent to test
		'''

		self.agent = RucaptchaImageAgent('API KEY', 'USD')

	def test_init(self):
		'''
		Tests that the RucaptchaImageAgent initializes correctly
		'''

		self.assertNotEqual(self.agent._cost, 0.0)
		self.assertIsInstance(self.agent._cost, float)

	@mock.patch(
		'caboodle.agents.rucaptcha.lib.get',
		side_effect = lambda *args, **kwags: 'Python'
	)
	@mock.patch(
		'caboodle.agents.rucaptcha.lib.post_image',
		side_effect = lambda *args, **kwags: 42
	)
	def test_solve(self, mock_post, mock_get):
		'''
		Tests that the RucaptchaImageAgent solves a Challenge correctly
		'''

		data = {
			'columns': None,
			'rows': None
		}

		self.assertEqual(self.agent.solve(data), 'fail')

		if PYTHON:
			data = {
				'image': PYTHON
			}

			self.agent.solve(data)
			self.assertEqual(data['id'], 42)
			self.assertEqual(data['result'], 'Python')

			with self.assertRaises(TypeError):
				self.agent.solve(None)
		else:
			self.fail('Could not locate data file')

	def test_cost(self):
		'''
		Tests that the RucaptchaImageAgent returns the correct cost
		'''

		self.assertNotEqual(self.agent.get_cost(), 0.0)
		self.assertIsInstance(self.agent.get_cost(), float)

	def test_comparable(self):
		'''
		Tests that a RucaptchaImageAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a RucaptchaImageAgent can handle a successful Challenge
		correctly
		'''

		if PYTHON:
			data = {
				'image': PYTHON,
				'id': 42
			}

			self.agent.success(data)
		else:
			self.fail('Could not locate data file')

	def test_fail(self):
		'''
		Tests that a RucaptchaImageAgent can handle a failed Challenge correctly
		'''

		if PYTHON:
			data = {
				'image': PYTHON,
				'id': 42
			}

			self.agent.fail(data)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
