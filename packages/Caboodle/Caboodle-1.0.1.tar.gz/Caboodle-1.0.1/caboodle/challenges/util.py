'''
Utility Functions for Challenges

This module defines useful and frequently used functions for use in Challenges.
Import this module to use them.
'''

from caboodle import web
from io import BytesIO
from PIL import Image
import base64
import requests
import pyscreenshot as ImageGrab

def _process_video_captcha(image):
	'''
	Processes Solve Media Video CAPTCHA

	Args:
		image (bytes): The overlay image encoded in base64

	Returns:
		A base64 encoded JPEG image

	The image processing includes cropping the overlay image to extract the
	bottom 20 pixels, adding a 10 pixel black border and scaling everything by a
	factor of 2.
	'''

	result = BytesIO()

	image = BytesIO(base64.b64decode(image))
	image = Image.open(image)
	image = image.convert('L').crop((0, 130, 300, 150)).crop((0, -10, 300, 30))
	image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
	image.save(result, format = 'JPEG')

	return base64.b64encode(result.getvalue())

def _process_reveal_captcha(image):
	'''
	Processes Solve Media Reveal CAPTCHA

	Args:
		image (bytes): The overlay image encoded in base64

	Returns:
		A base64 encoded JPEG image

	The image processing includes adding a 10 pixel black border and scaling
	everything by a factor of 2.
	'''

	result = BytesIO()

	image = BytesIO(base64.b64decode(image))
	image = Image.open(image).crop((0, -10, 300, 30))
	image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
	image.save(result, format = 'JPEG')

	return base64.b64encode(result.getvalue())

def get_element_image(element, browser):
	'''
	Takes a screenshot and crops out the element

	Args:
		element (WebElement): The element to crop
		browser (Browser): The web browser to use

	Returns:
		A base64 encoded JPEG image
	'''

	result = BytesIO()

	x, y = int(element.location['x']), int(element.location['y'])
	w, h = int(element.size['width']), int(element.size['height'])

	screen = BytesIO(base64.b64decode(browser.get_screenshot_as_base64()))
	image = Image.open(screen).crop((x, y, x + w, y + h))
	background = Image.new('RGB', image.size, (255, 255, 255))
	background.paste(image, mask = image.split()[3])
	background.save(result, format = 'JPEG')

	return base64.b64encode(result.getvalue())

def get_image_src(element):
	'''
	Downloads the source of an image

	Args:
		element (WebElement): The element to download

	Returns:
		A base64 encoded image
	'''

	return base64.b64encode(requests.get(element.get_attribute('src')).content)

def get_image_from_swf(url, timeout = 5):
	'''
	Takes a screenshot of a Flash object (.swf)

	Args:
		url (str): The URL of the SWF
		timeout (int): The length of time to wait before taking the screenshot

	Returns:
		A base64 encoded JPEG image
	'''

	result = BytesIO()

	browser = web.Browser()
	browser.set_timeout(timeout)
	browser.maximize_window()
	browser.get(url)
	bbox = browser.execute_script(
		'''
		var xy = [
			window.screenX + (window.outerWidth - window.innerWidth),
			window.screenY + (window.outerHeight - window.innerHeight)
		];
		var wh = [
			xy[0] + window.innerWidth,
			xy[1] + window.innerHeight
		];
		return xy.concat(wh);
		'''
	)
	ImageGrab.grab(bbox = bbox).save(result, format = 'JPEG')
	browser.quit()

	return base64.b64encode(result.getvalue())
