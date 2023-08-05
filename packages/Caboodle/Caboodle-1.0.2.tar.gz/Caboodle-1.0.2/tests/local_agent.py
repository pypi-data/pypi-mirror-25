from caboodle.agents.local import LocalAgent
import os
import sys
import unittest

INPUT = None

# Locate data file and read it
for root, dirs, files in os.walk(os.getcwd()):
	if 'input' in files:
		INPUT = os.path.join(root, 'input')
		INPUT = open(INPUT, 'r')

class LocalAgentTest(unittest.TestCase):
	'''
	Tests the LocalAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a LocalAgent to test
		'''

		self.agent = LocalAgent()

	def test_init(self):
		'''
		Tests that the LocalAgent initializes correctly
		'''

		self.assertEqual(self.agent._cost, 0.0)

	def test_solve(self):
		'''
		Tests that the LocalAgent solves a Challenge correctly
		'''

		# Override stdin
		stdin = sys.stdin
		sys.stdin = INPUT

		data = {'text': 'What is the answer to the question?'}

		self.agent.solve(data)
		self.assertEqual(data['result'], '42')

		with self.assertRaises(TypeError):
			self.agent.solve(None)

		# Restore stdin
		sys.stdin = stdin

	def test_cost(self):
		'''
		Tests that the LocalAgent returns the correct cost
		'''

		self.assertEqual(self.agent.get_cost(), 0.0)

	def test_comparable(self):
		'''
		Tests that a LocalAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a LocalAgent can handle a successful Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 42
		}

		self.assertFalse(self.agent.success(data))

	def test_fail(self):
		'''
		Tests that a LocalAgent can handle a failed Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 3.14
		}

		self.assertFalse(self.agent.fail(data))

if __name__ == '__main__':
	unittest.main()
