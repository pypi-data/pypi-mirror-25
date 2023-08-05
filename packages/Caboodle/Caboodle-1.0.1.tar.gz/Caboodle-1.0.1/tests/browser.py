from caboodle import web
import unittest

class BrowserTest(unittest.TestCase):
	'''
	Tests the Browser to verify that it works correctly
	'''

	@classmethod
	def setUpClass(self):
		'''
		Creates a Browser to test
		'''

		self.browser = web.Browser()

	def test_init(self):
		'''
		Tests that the Browser initializes correctly
		'''

		self.assertTrue(self.browser.driver)

	def test_proxy(self):
		'''
		Tests that the Browser creates a proxy correctly
		'''

		with self.assertRaises(ValueError):
			web.Browser('invalid_proxy')

		with self.assertRaises(ValueError):
			web.Browser('invalid:proxy')

		browser = web.Browser('127.0.0.1:1234')
		browser.get('https://www.google.com')
		browser.quit()

	def test_get(self):
		'''
		Tests that the Browser can get a URL correctly
		'''

		self.browser.get('https://www.google.com')

		self.assertTrue(self.browser.find_element_by_name('q'))

	def test_actionchains(self):
		'''
		Tests that the Browser can create an ActionChains object
		'''

		self.browser.action().perform()

	def test_timeout(self):
		'''
		Tests that the Browser handles page load timeouts correctly
		'''

		self.browser.set_timeout(0)

		self.browser.get('https://www.google.com')

		with self.assertRaises(ValueError):
			self.browser.set_timeout('abc')

		self.browser.set_timeout(30)

	@classmethod
	def tearDownClass(self):
		'''
		Closes the Browser to end the test
		'''

		self.browser.quit()

if __name__ == '__main__':
	unittest.main()
