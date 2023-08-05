Spec
====

Specifications for Challenge objects

This module defines abstract classes with compounding levels of functionality.
Every Challenge should have a `get_data()` and `submit_data()` function. These
specifications can not be instantiated and can only be used by a subclass that
implements all of the required functions. Be sure, however, to explicitly call
the `super()` function from each subclass and from each defined function in
that subclass to gain the functionality of it's parent. See the unit tests for
this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Challenge(object)

An object that represents a challenge

A Challenge collects data and packages it into a dictionary to be processed.
Once that data has been processed, it can then submit the result in the
required way. As a general guideline, processed data should contain a key
named 'result' and so a Challenge may depend on that when submitting. In
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
