from setuptools import setup, find_packages

def format(input, start = 0):
	result = ''
	indent = False
	count = 0

	with open(input, 'r') as file:
		for line in file:
			if count > start:
				if line[:1] == '\t' and not indent:
					indent = True
					result += '::\n\n'

				if line[:1].isalnum() and indent:
					indent = False

				result += line.replace('> ', '\t').replace('>', '')
			count += 1

	return result

blurb = ('Caboodle is a Python module for web browsing, web scraping or web '
	'automation developed to provide an all-in-one (kit and caboodle) utility '
	'for anything the web has to offer.\n'
)

setup(
	name = 'Caboodle',
	version = '1.0.2',
	author = 'Justin Willis',
	author_email = 'sirJustin.Willis@gmail.com',
	packages = find_packages(),
	url = 'https://bitbucket.org/bkvaluemeal/caboodle',
	license = 'ISC License',
	description =
		'A Python module for web browsing, web scraping or web automation',
	long_description = blurb + format('README.md', 3),
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Other/Nonlisted Topic'
	],
	keywords = 'web browsing scraping automation',
	install_requires = [
		'Pillow',
		'pyscreenshot',
		'Requests',
		'Selenium'
	]
)
