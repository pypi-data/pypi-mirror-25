Solve_Media
===========

Solve Media CAPTCHA Challenges

This module is an implementation of the Challenge specification and collects
data to solve Solve Media CAPTCHAs. To use these Challenges, create a new
instance of them and call the `get_data()` function. Then, process the data
using an Agent and submit it by calling the `submit_data()` function. See the
unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### SolveMediaEmbedChallenge(caboodle.challenges.spec.Challenge)

A Challenge for Solve Media Embed CAPTCHAs

An embed CAPTCHA is a type of CAPTCHA where the user is presented with an
embedded flash object and must enter the text it contains. This Challenge
will locate it if it exists and add a base64 encoded image of it to the
dictionary with the key 'image'. In addition to the image, the form to enter
the result and the reload button to get a new CAPTCHA are added to the
dictionary with the keys 'form' and 'reload' respectively.

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


### SolveMediaRevealChallenge(caboodle.challenges.spec.Challenge)

A Challenge for Solve Media Reveal CAPTCHAs

A reveal CAPTCHA is a type of CAPTCHA where the user is blatantly given a
text to type. This Challenge will locate it if it exists and add a base64
encoded image of it to the dictionary with the key 'image'. In addition to
the image, the form to enter the result and the reload button to get a new
CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
respectively.

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


### SolveMediaTextChallenge(caboodle.challenges.spec.Challenge)

A Challenge for Solve Media Text CAPTCHAs

A text CAPTCHA is the traditional type of CAPTCHA with obfuscated squiggly
text. This Challenge will locate it if it exists and add a base64 encoded
image of the CAPTCHA to the dictionary with the key 'image'. In addition to
the CAPTCHA, the form to enter the result and the reload button to get a new
CAPTCHA are added to the dictionary with the keys 'form' and 'reload'
respectively.

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


### SolveMediaVideoChallenge(caboodle.challenges.spec.Challenge)

A Challenge for Solve Media Video CAPTCHAs

A video CAPTCHA is a unique type of CAPTCHA where the user must watch a
short video before given the text to type in. This Challenge will locate the
text if it exists and add a base64 encoded image of it to the dictionary
with the key 'image'. In addition to the text, the form to enter the result
and the reload button to get a new CAPTCHA are added to the dictionary with
the keys 'form' and 'reload' respectively.

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
