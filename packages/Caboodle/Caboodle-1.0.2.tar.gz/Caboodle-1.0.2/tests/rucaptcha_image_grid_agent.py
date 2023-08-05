from caboodle.agents.rucaptcha import RucaptchaImageGridAgent
from unittest import mock
import os
import unittest

TRUCKS = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'commercial_trucks' in files:
		TRUCKS = os.path.join(root, 'commercial_trucks')
		TRUCKS = open(TRUCKS, 'rb').read()

class RucaptchaImageGridAgentTest(unittest.TestCase):
	'''
	Tests the RucaptchaImageGridAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a RucaptchaImageGridAgent to test
		'''

		self.agent = RucaptchaImageGridAgent('API KEY', 'USD')

	def test_init(self):
		'''
		Tests that the RucaptchaImageGridAgent initializes correctly
		'''

		self.assertNotEqual(self.agent._cost, 0.0)
		self.assertIsInstance(self.agent._cost, float)

	@mock.patch(
		'caboodle.agents.rucaptcha.lib.get',
		side_effect = lambda *args, **kwags: 'click:1/4/5'
	)
	@mock.patch(
		'caboodle.agents.rucaptcha.lib.post_image_grid',
		side_effect = lambda *args, **kwags: 42
	)
	def test_solve(self, mock_post, mock_get):
		'''
		Tests that the RucaptchaImageGridAgent solves a Challenge correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'text': 'Select all images with commercial trucks',
				'rows': 3,
				'columns': 3
			}

			self.agent.solve(data)
			self.assertEqual(data['id'], 42)
			self.assertEqual(data['result'], (0, 3, 4))

			with self.assertRaises(TypeError):
				self.agent.solve(None)
		else:
			self.fail('Could not locate data file')

	def test_cost(self):
		'''
		Tests that the RucaptchaImageGridAgent returns the correct cost
		'''

		self.assertNotEqual(self.agent.get_cost(), 0.0)
		self.assertIsInstance(self.agent.get_cost(), float)

	def test_comparable(self):
		'''
		Tests that a RucaptchaImageGridAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a RucaptchaImageGridAgent can handle a successful Challenge
		correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'text': 'Select all images with commercial trucks',
				'rows': 3,
				'columns': 3,
				'id': 42
			}

			self.agent.success(data)
		else:
			self.fail('Could not locate data file')

	def test_fail(self):
		'''
		Tests that a RucaptchaImageGridAgent can handle a failed Challenge
		correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'text': 'Select all images with commercial trucks',
				'rows': 3,
				'columns': 3,
				'id': 42
			}

			self.agent.fail(data)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
