from caboodle.agents.d3cryp7 import d3cryp7TagImageGridAgent
import os
import unittest

TRUCKS = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'commercial_trucks' in files:
		TRUCKS = os.path.join(root, 'commercial_trucks')
		TRUCKS = open(TRUCKS, 'rb').read()

class d3cryp7TagImageGridAgentTest(unittest.TestCase):
	'''
	Tests the d3cryp7TagImageGridAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a d3cryp7TagImageGridAgent to test
		'''

		self.agent = d3cryp7TagImageGridAgent('http://localhost')

	def test_init(self):
		'''
		Tests that the d3cryp7TagImageGridAgent initializes correctly
		'''

		self.assertEqual(self.agent._cost, 0.0)
		self.assertIsInstance(self.agent._cost, float)

	def test_solve(self):
		'''
		Tests that the d3cryp7TagImageGridAgent solves a Challenge correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'tag': 'truck',
				'columns': 3,
				'rows': 3,
				'ids': (0,)
			}

			self.agent.solve(data)
			self.assertEqual(type(data['result']), tuple)

			data = {
				'image': None,
				'tag': '',
				'columns': 3,
				'rows': 3,
				'ids': (0,)
			}

			with self.assertRaises(RuntimeError):
				self.agent.solve(data)

			with self.assertRaises(TypeError):
				self.agent.solve(None)
		else:
			self.fail('Could not locate data file')

	def test_cost(self):
		'''
		Tests that the d3cryp7TagImageGridAgent returns the correct cost
		'''

		self.assertEqual(self.agent.get_cost(), 0.0)
		self.assertIsInstance(self.agent.get_cost(), float)

	def test_comparable(self):
		'''
		Tests that a d3cryp7TagImageGridAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a d3cryp7TagImageGridAgent can handle a successful Challenge
		correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'ids': (0,)
			}

			self.agent.success(data)
		else:
			self.fail('Could not locate data file')

	def test_fail(self):
		'''
		Tests that a d3cryp7TagImageGridAgent can handle a failed Challenge correctly
		'''

		if TRUCKS:
			data = {
				'image': TRUCKS,
				'ids': (0,)
			}

			self.agent.fail(data)
		else:
			self.fail('Could not locate data file')

if __name__ == '__main__':
	unittest.main()
