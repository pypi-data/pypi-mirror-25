'''
ruCaptcha Library

The ruCaptcha library defines functions to interact with ruCaptcha's web API.
See the unit tests for this library for more information.
'''

from io import BytesIO
from PIL import Image
import base64
import json
import requests
import time

def post_image(key, image):
	'''
	Posts an image to be solved

	Args:
		key (str): The API key to use
		image (bytes): The base64 encoded image to post

	Returns:
		The ID of the posted image

	Raises:
		RuntimeError: The post failed
	'''

	data = {
		'method': 'base64',
		'key': key,
		'body': scale_image(image)
	}

	r = requests.post('http://rucaptcha.com/in.php', data = data)

	if r.ok:
		if '|' in r.text:
			response, id = r.text.split('|', 1)

			if response == 'OK':
				return id
			else:
				raise RuntimeError(r.text)
		else:
			raise RuntimeError(r.text)
	else:
		raise RuntimeError('Error %d' % r.status_code)

def post_image_grid(key, image, text, rows, columns):
	'''
	Posts an image grid to be solved

	Args:
		key (str): The API key to use
		image (bytes): The base64 encoded image to post
		text (str): The instructions for the image
		rows (int): The number of rows
		columns (int): The number of columns

	Returns:
		The ID of the posted image

	Raises:
		RuntimeError: The post failed
	'''

	data = {
		'method': 'base64',
		'key': key,
		'recaptcha': 1,
		'textinstructions': text,
		'body': image,
		'row': rows,
		'column': columns
	}

	r = requests.post('http://rucaptcha.com/in.php', data = data)

	if r.ok:
		if '|' in r.text:
			response, id = r.text.split('|', 1)

			if response == 'OK':
				return id
			else:
				raise RuntimeError(r.text)
		else:
			raise RuntimeError(r.text)
	else:
		raise RuntimeError('Error %d' % r.status_code)

def get(key, id):
	'''
	Gets the result of a posted image

	Args:
		key (str): The API key to use
		id (str): The ID of the posted image

	Returns:
		The result of the posted image

	Raises:
		RuntimeError: The get failed
	'''

	params = {
		'key': key,
		'action': 'get',
		'id': id
	}

	while True:
		r = requests.get('http://rucaptcha.com/res.php', params = params)

		if r.ok:
			if '|' in r.text:
				return r.text.split('|', 1)[1]
			elif r.text == 'CAPCHA_NOT_READY':
				pass
			else:
				raise RuntimeError(r.text)
		else:
			raise RuntimeError('Error %d' % r.status_code)

		time.sleep(5)

def invalid(key, id):
	'''
	Reports a posted image as invalid

	Args:
		key (str): The API key to use
		id (str): The ID of the posted image
	'''

	params = {
		'key': key,
		'action': 'reportbad',
		'id': id
	}

	while True:
		r = requests.get('http://rucaptcha.com/res.php', params = params)

		if r.ok:
			break
		else:
			time.sleep(1)

def get_rate(currency, rate = 0.0):
	'''
	Calculates the solving rate in any currency

	Args:
		currency (str): The currency to convert to
		rate (float): A constant solving rate

	Returns:
		The solving rate as a floating point number

	The currency must be a three letter code like USD or EUR. If `rate` is set,
	it will override the rate received from ruCaptcha's API.
	'''

	while rate == 0.0:
		r = requests.get('http://rucaptcha.com/load.php')

		if r.ok:
			rate = r.text.split('\r\n')[3]
			rate = rate.split('>')[1]
			rate = rate.split('<')[0]
			rate = float(rate)

			break
		else:
			time.sleep(1)

	while currency is not 'RUB':
		r = requests.get('http://api.fixer.io/latest?base=RUB')

		if r.ok:
			rates = json.loads(r.text)
			rate *= rates['rates'][currency]

			break
		else:
			time.sleep(1)

	return rate

def scale_image(image):
	'''
	Scales a base64 encoded image to meet ruCaptcha's requirements

	Args:
		image (bytes): The base64 encoded image

	Returns:
		A base64 encoded JPEG image
	'''

	result = BytesIO()
	image = BytesIO(base64.b64decode(image))
	image = Image.open(image)

	w, h = image.size
	scale = 400 / (w + h)

	image = image.resize((int(scale * w), int(scale * h)), Image.ANTIALIAS)
	image.save(result, format = 'JPEG')

	return base64.b64encode(result.getvalue())
