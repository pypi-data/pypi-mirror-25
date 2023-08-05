Manual
======

A manually defined Challenge

This module is an implementation of the Challenge specification and collects
data using an external function defined by the user. To use this Challenge,
create a new instance of it with the desired functions and call the `get_data()`
function. Then, process the data using an Agent and submit it by calling the
`submit_data()` function. See the unit tests for this module for more
information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### ManualChallenge(caboodle.challenges.spec.Challenge)

A Challenge that uses external functions

**Args:**

|      Name       |   Type   |         Description          |
|-----------------|----------|------------------------------|
| get_function    | Function | The function to collect data |
| submit_function | Function | The function to submit data  |

**Raises:**

|   Type    |           Description           |
|-----------|---------------------------------|
| TypeError | The arguments are not functions |

As a general guideline, processed data should contain a key named 'result'
and so the `submit_function` may depend on that when submitting. In
addition, collected data should be organized logically. For example, if the
Challenge requires an image to be solved, it should be base64 encoded and
appended to the dictionary with the key 'image'.

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
