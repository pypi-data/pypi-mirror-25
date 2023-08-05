'''
Web Interfaces

This module defines objects for interacting with the World Wide Web. See the
documentation for each object and their respective unit tests for more
information.
'''

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains

class Browser(object):
	'''
	A web browser

	Args:
		proxy (str): The proxy to use

	Raises:
		ValueError: The proxy is invalid

	Browser is a wrapper for the web browser automation tool Selenium. To
	simplify things and to avoid linking to external binaries, only Firefox
	is supported. Firefox natively supports Selenium without any configuration.

	A proxy may be used and must be in the form of `host:port`. The host
	can be a fully qualified domain name (FQDN) or an IP address. The port
	must be a valid integer. You may also set the proxy to None for no proxy.

	Example:

		127.0.0.1:3128
		localhost:3128
		None
	'''

	def __init__(self, proxy = None):
			if proxy:
				if proxy.count(':') is not 1:
					raise ValueError('Proxy %s is invalid' % proxy)

				port = proxy.split(':')[1]
				try:
					int(port)
				except:
					raise ValueError('Proxy port %s is invalid' % port)

				proxy = Proxy({
					'proxyType': ProxyType.MANUAL,
					'httpProxy': proxy,
					'ftpProxy': proxy,
					'sslProxy': proxy
				})

				self.driver = webdriver.Firefox(proxy = proxy)
			else:
				self.driver = webdriver.Firefox()

	def __getattr__(self, attr):
		return self.driver.__getattribute__(attr)

	def get(self, url):
		'''
		Requests a URL in the browser

		Args:
			url (str): The URL to request

		If the page load time exceeds the default timeout limit, it will
		automatically be handled by forcing the Browser to stop loading.
		You can set the default timeout with the `set_timeout()` function.
		'''

		try:
			self.driver.get(url)
		except TimeoutException:
			self.driver.execute_script('window.stop();')

	def action(self):
		'''
		Creates an ActionChains object to string together operations

		Returns:
			An ActionChains object

		An action chain is useful for doing complex actions like hover over
		and drag and drop. This function returns an ActionChains object with
		the Browser passed as an argument and can be used just like the
		original found here:

		http://selenium-python.readthedocs.io/api.html
		'''

		return ActionChains(self.driver)

	def set_timeout(self, time):
		'''
		Changes the length of time a page is allowed to load before it stops

		Args:
			time (int): The page load time in seconds

		Raises:
			ValueError: The page load time is invalid
		'''

		if type(time) is int:
			self.driver.set_page_load_timeout(time)
		else:
			raise ValueError('%s is an invalid time' % time)
