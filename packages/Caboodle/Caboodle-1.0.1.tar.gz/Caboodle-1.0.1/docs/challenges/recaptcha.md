Recaptcha
=========

ReCAPTCHA CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve ReCAPTCHA CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### RecaptchaV2Challenge(caboodle.challenges.spec.Challenge)

A Challenge for ReCAPTCHA v2 CAPTCHAs

Version 2 of ReCAPTCHA is the common "I'm not a robot" CAPTCHA where you are
prompted to choose a selection of images from a grid. This Challenge will
locate the grid of images and add the aggregate of all the images to the
dictionary with the key 'image'. In addition to the CAPTCHA, the elements to
click, the verify button, the text instructions, the type of image to look
for, the reload button to get a new CAPTCHA and the dimensions of the image
grid are added to the dictionary with the keys 'tiles', 'verify', 'text',
'tag', 'reload', 'columns' and 'rows' respectively.

#### get_data(browser)

Collects data needed to solve the Challenge

**Args:**

|  Name   |  Type   |      Description       |
|---------|---------|------------------------|
| browser | Browser | The web browser to use |

**Returns:**

|    Type    |          Description           |
|------------|--------------------------------|
| Dictionary | A dictionary of collected data |

**Raises:**

|   Type    |            Description             |
|-----------|------------------------------------|
| TypeError | The browser is not of type Browser |

#### submit_data(data)

Submits the processed data and solves the Challenge

**Args:**

| Name |    Type    |       Description       |
|------|------------|-------------------------|
| data | Dictionary | The Challenge to submit |

**Raises:**

|   Type    |         Description          |
|-----------|------------------------------|
| TypeError | The data is not a dictionary |
