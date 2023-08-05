from caboodle.agents.manual import ManualAgent
import unittest

def foo(data):
	'''
	Solves a Challenge and stores the result

	Args:
		data (dict): The Challenge to solve

	Raises:
		TypeError: The Challenge is not a dictionary
		ValueError: The Challenge does not contain the required data
		RuntimeError: The Challenge could not be solved
	'''

	if data:
		data['result'] = 42
	else:
		raise TypeError('The Challenge must be a dictionary')

class ManualAgentTest(unittest.TestCase):
	'''
	Tests the ManualAgent to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a ManualAgent to test
		'''

		self.agent = ManualAgent(
			foo,
			lambda data: True,
			lambda data: False
		)

	def test_init(self):
		'''
		Tests that the ManualAgent initializes correctly
		'''

		self.assertEqual(self.agent._cost, 0.0)

		with self.assertRaises(TypeError):
			ManualAgent(
				None,
				lambda data: type(data),
				lambda data: type(data)
			)

		with self.assertRaises(TypeError):
			ManualAgent(
				lambda data: type(data),
				None,
				lambda data: type(data)
			)

		with self.assertRaises(TypeError):
			ManualAgent(
				lambda data: type(data),
				lambda data: type(data),
				None
			)

	def test_solve(self):
		'''
		Tests that the ManualAgent solves a Challenge correctly
		'''

		data = {'text': 'What is the answer to the question?'}

		self.agent.solve(data)
		self.assertEqual(data['result'], 42)

		with self.assertRaises(TypeError):
			self.agent.solve(None)

	def test_cost(self):
		'''
		Tests that the ManualAgent returns the correct cost
		'''

		self.assertEqual(self.agent.get_cost(), 0.0)

	def test_comparable(self):
		'''
		Tests that a ManualAgent can be compared to another Agent
		'''

		self.assertFalse(self.agent < self.agent)

		with self.assertRaises(TypeError):
			self.agent < None

	def test_success(self):
		'''
		Tests that a ManualAgent can handle a successful Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 42
		}

		self.assertTrue(self.agent.success(data))

	def test_fail(self):
		'''
		Tests that a ManualAgent can handle a failed Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 3.14
		}

		self.assertFalse(self.agent.fail(data))

if __name__ == '__main__':
	unittest.main()
