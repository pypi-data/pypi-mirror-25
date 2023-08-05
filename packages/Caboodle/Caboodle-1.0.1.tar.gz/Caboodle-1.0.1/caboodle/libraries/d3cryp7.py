'''
d3cryp7 Library

The d3cryp7 library defines functions to interact with d3cryp7's web API.
See the unit tests for this library for more information.
'''

from io import BytesIO
from PIL import Image
import base64
import json
import requests
import time

def recognize_image(url, image):
	'''
	Posts an image to be recognized

	Args:
		url (str): The URL of the d3cryp7 API
		image (bytes): The base64 encoded image to post

	Returns:
		A string containing the text in the image

	Raises:
		RuntimeError: The post failed
	'''

	data = {
		'image': image
	}

	r = requests.post(url + '/api/recognize', data = data)

	if r.ok:
		response = r.json()

		if response['result'] and len(response['result']) > 0:
			return response['result'], response['id']
		else:
			raise RuntimeError('No result')
	else:
		raise RuntimeError('Error %d' % r.status_code)

def tag_image(url, image):
	'''
	Posts an image to be tagged

	Args:
		url (str): The URL of the d3cryp7 API
		image (bytes): The base64 encoded image to post

	Returns:
		A dictionary of tags and their probabilities

	Raises:
		RuntimeError: The post failed
	'''

	data = {
		'image': image
	}

	r = requests.post(url + '/api/tag', data = data)

	if r.ok:
		response = r.json()

		if response['result'] and len(response['result']) > 0:
			return response['result'], response['id']
		else:
			raise RuntimeError('No result')
	else:
		raise RuntimeError('Error %d' % r.status_code)

def tag_image_grid(url, image, col, row):
	'''
	Posts an image grid to be tagged

	Args:
		url (str): The URL of the d3cryp7 API
		image (bytes): The base64 encoded image to post
		col (int): The number of columns in the image
		row (int): The number of rows in the image

	Returns:
		A tuple of dictionaries of tags and their probabilities

	Raises:
		RuntimeError: The post failed
	'''

	if not image:
		raise RuntimeError('Image cannot be null')

	result = ()
	ids = ()
	im = Image.open(BytesIO(base64.b64decode(image)))
	w, h = im.size
	bbs = generate_bbs(w, h, col, row)

	for bb in bbs:
		im2 = BytesIO()
		temp = im.crop(bb)
		temp.save(im2, format = 'JPEG')
		im2 = base64.b64encode(im2.getvalue())
		response, id = tag_image(url, im2)
		result += (response,)
		ids += (id,)

	return result, ids

def generate_bbs(w, h, col, row):
	'''
	Generates a tuple of bounding boxes to crop a grid of images

	Args:
		w (int): The width of an image
		h (int): The height of an image
		col (int): The number of columns in an image
		row (int): The number of rows in an image

	Returns:
		A tuple of tuples that contain 4 integers
	'''

	cell_w = w / col
	cell_h = h / row

	return tuple(
		(
			int(cell_w * j), int(cell_h * i),
			int(cell_w * j + cell_w), int(cell_h * i + cell_h)
		)
		for i in range(row)
		for j in range(col)
	)

def get_rate(url, currency):
	'''
	Calculates the solving rate in any currency

	Args:
		url (str): The URL of the d3cryp7 API
		currency (str): The currency to convert to

	Returns:
		A dictionary of solving rates as floating point numbers

	The currency must be a three letter code like USD or EUR.
	'''

	rate = None

	while not rate:
		r = requests.get(url + '/api/cost')

		if r.ok:
			rate = json.loads(r.text)

			break
		else:
			time.sleep(1)

	while currency is not 'USD':
		r = requests.get('http://api.fixer.io/latest?base=USD')

		if r.ok:
			rates = json.loads(r.text)

			for key in rate.keys():
				rate[key] *= rates['rates'][currency]

			break
		else:
			time.sleep(1)

	return rate

def success(url, id):
	'''
	Reports a posted image as successful

	Args:
		url (str): The URL of the d3cryp7 API
		id (str): The ID of the posted image
	'''

	data = {
		'id': id
	}

	while True:
		r = requests.post(url + '/api/set_success', data = data)

		if r.ok:
			break
		else:
			time.sleep(1)

def invalid(url, id):
	'''
	Reports a posted image as invalid

	Args:
		url (str): The URL of the d3cryp7 API
		id (str): The ID of the posted image
	'''

	data = {
		'id': id
	}

	while True:
		r = requests.post(url + '/api/set_fail', data = data)

		if r.ok:
			break
		else:
			time.sleep(1)
