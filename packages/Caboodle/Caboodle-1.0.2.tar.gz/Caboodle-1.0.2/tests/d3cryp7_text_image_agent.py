from caboodle.agents.d3cryp7 import d3cryp7TextImageAgent
import os
import unittest

PANGRAM = None
HELLO_WORLD = None
TRUCKS = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'pangram' in files:
		PANGRAM = os.path.join(root, 'pangram')
		PANGRAM = open(PANGRAM, 'rb').read()

	if 'hello_world' in files:
		HELLO_WORLD = os.path.join(root, 'hello_world')
		HELLO_WORLD = open(HELLO_WORLD, 'rb').read()

	if 'commercial_trucks' in files:
		TRUCKS = os.path.join(root, 'commercial_trucks')
		TRUCKS = open(TRUCKS, 'rb').read()

class d3cryp7TextImageAgentTest(unittest.TestCase):
	'''
	Tests the d3cryp7TextImageAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a d3cryp7TextImageAgent to test
		'''

		self.agent = d3cryp7TextImageAgent('http://localhost')

	def test_init(self):
		'''
		Tests that the d3cryp7TextImageAgent initializes correctly
		'''

		self.assertEqual(self.agent._cost, 0.0)
		self.assertIsInstance(self.agent._cost, float)

	def test_solve(self):
		'''
		Tests that the d3cryp7TextImageAgent solves a Challenge correctly
		'''

		data = {
			'columns': None,
			'rows': None
		}

		self.assertEqual(self.agent.solve(data), 'fail')

		if HELLO_WORLD and PANGRAM and TRUCKS:
			data = {
				'image': PANGRAM
			}

			self.agent.solve(data)
			self.assertEqual(
				data['result'],
				'The quick brown fox jumps over the lazy dog.'
			)

			data = {
				'image': HELLO_WORLD
			}

			self.agent.solve(data)
			self.assertEqual(data['result'], 'Hello\nWorld')

			data = {
				'image': TRUCKS
			}

			with self.assertRaises(RuntimeError):
				self.agent.solve(data)

			data = {
				'image': None
			}

			with self.assertRaises(RuntimeError):
				self.agent.solve(data)

			with self.assertRaises(TypeError):
				self.agent.solve(None)
		else:
			self.fail('Could not locate data file')

	def test_cost(self):
		'''
		Tests that the d3cryp7TextImageAgent returns the correct cost
		'''

		self.assertEqual(self.agent.get_cost(), 0.0)
		self.assertIsInstance(self.agent.get_cost(), float)

	def test_comparable(self):
		'''
		Tests that a d3cryp7TextImageAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a d3cryp7TextImageAgent can handle a successful Challenge
		correctly
		'''

		if HELLO_WORLD:
			data = {
				'image': HELLO_WORLD,
				'id': 0
			}

			self.agent.success(data)
		else:
			self.fail('Could not locate data file')

	def test_fail(self):
		'''
		Tests that a d3cryp7TextImageAgent can handle a failed Challenge correctly
		'''

		if PANGRAM:
			data = {
				'image': PANGRAM,
				'id': 0
			}

			self.agent.fail(data)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
