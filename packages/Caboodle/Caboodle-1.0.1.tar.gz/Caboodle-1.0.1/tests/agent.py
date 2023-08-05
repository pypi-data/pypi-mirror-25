from caboodle.agents.spec import Agent
import unittest

class GoodAgent(Agent):
	'''
	A complete child of the Agent specification
	'''

	def __init__(self):
		super().__init__()

		self._cost = 3.14

	def solve(self, data):
		'''
		Solves a Challenge and stores the result

		Args:
			data (dict): The Challenge to solve

		Raises:
			TypeError: The Challenge is not a dictionary
		'''

		super().solve(data)

		data['result'] = 42

	def get_cost(self):
		'''
		Returns the cost of using this Agent

		Returns:
			The cost as a floating point number
		'''

		super().get_cost()

		return self._cost

	def success(self, data):
		'''
		Performs actions for a successful Challenge

		Args:
			data (dict): The successful Challenge
		'''

		super().success(data)

		return True

	def fail(self, data):
		'''
		Performs actions for a failed Challenge

		Args:
			data (dict): The failed Challenge
		'''

		super().fail(data)

		return False

class BadAgent(Agent):
	'''
	An incomplete child of the Agent specification
	'''

	def __init__(self):
		super().__init__()

class AgentTest(unittest.TestCase):
	'''
	Tests the Agent specification to verify that it works correctly
	'''

	def test_abstraction(self):
		'''
		Tests that an incomplete child of the Agent specification will
		raise a TypeError
		'''

		with self.assertRaises(TypeError):
			BadAgent()

	def test_init(self):
		'''
		Tests that the Agent specification initializes correctly
		'''

		self.assertIsInstance(GoodAgent(), Agent)
		self.assertEqual(GoodAgent()._cost, 3.14)

	def test_solve(self):
		'''
		Tests that the Agent specification solves a Challenge correctly
		'''

		data = {'text': 'What is the answer to the question?'}

		GoodAgent().solve(data)
		self.assertEqual(data['result'], 42)

		with self.assertRaises(TypeError):
			GoodAgent().solve(None)

	def test_cost(self):
		'''
		Tests that the Agent specification returns the correct cost
		'''

		self.assertEqual(GoodAgent().get_cost(), 3.14)

	def test_comparable(self):
		'''
		Tests that an Agent can be compared to another Agent
		'''

		self.assertFalse(GoodAgent() < GoodAgent())

		with self.assertRaises(TypeError):
			GoodAgent() < None

	def test_success(self):
		'''
		Tests that an Agent can handle a successful Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 42
		}

		self.assertTrue(GoodAgent().success(data))

	def test_fail(self):
		'''
		Tests that an Agent can handle a failed Challenge correctly
		'''

		data = {
			'text': 'What is the answer to the question?',
			'result': 3.14
		}

		self.assertFalse(GoodAgent().fail(data))

if __name__ == '__main__':
	unittest.main()
