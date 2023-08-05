from caboodle import web, solve
from caboodle.challenges.manual import ManualChallenge
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

	if 'image' in data:
		raise RuntimeError('The Challenge could not be solved')
	else:
		raise ValueError('The Challenge does not provide an image')

class SolverTest(unittest.TestCase):
	'''
	Tests the Solver to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Solver to test
		'''

		self.browser = web.Browser()
		self.solver = solve.Solver(self.browser)

	def test_init(self):
		'''
		Tests that the Solver initializes correctly
		'''

		self.assertTrue(self.solver.browser.driver)
		self.assertIsInstance(self.solver.challenges, list)
		self.assertIsInstance(self.solver.agents, list)

		with self.assertRaises(TypeError):
			solve.Solver(None)

	def test_solve(self):
		'''
		Tests that the Solver can solve a Challenge correctly given there are
		Challenges and Agents to solve those Challenges
		'''

		# Test adding null objects
		with self.assertRaises(TypeError):
			self.solver.add_challenge(None)

		with self.assertRaises(TypeError):
			self.solver.add_agent(None)

		# Test adding valid objects
		self.solver.add_challenge(
			ManualChallenge(
				lambda browser: {},
				lambda data: type(data)
			)
		)
		self.solver.add_challenge(
			ManualChallenge(
				lambda browser: {'text': 'What is the answer to the question?'},
				lambda data: self.assertEqual(data['result'], 42)
			)
		)
		self.assertEqual(len(self.solver.challenges), 2)

		self.solver.add_agent(
			ManualAgent(
				lambda data: 'fail',
				lambda data: self.assertTrue(data),
				lambda data: self.assertTrue(data)
			)
		)
		self.solver.add_agent(
			ManualAgent(
				foo,
				lambda data: self.assertTrue(data),
				lambda data: self.assertTrue(data)
			)
		)
		self.solver.add_agent(
			ManualAgent(
				lambda data: data.update({'result': 42}),
				lambda data: self.assertTrue(data),
				lambda data: self.assertTrue(data)
			)
		)
		self.assertEqual(len(self.solver.agents), 3)

		# Test challenge can be solved
		id = self.solver.solve()
		self.solver.set_success(id)
		self.assertEqual(len(self.solver.data), 0)

		with self.assertRaises(KeyError):
			self.solver.set_success('invalid key')

		id = self.solver.solve()
		self.solver.set_fail(id)
		self.assertEqual(len(self.solver.data), 0)

		with self.assertRaises(KeyError):
			self.solver.set_fail('invalid key')

		# Clear all agents
		del self.solver.agents[:]
		self.assertEqual(len(self.solver.agents), 0)

		# Test challenge can't be solved
		with self.assertRaises(RuntimeError):
			self.solver.solve()

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
