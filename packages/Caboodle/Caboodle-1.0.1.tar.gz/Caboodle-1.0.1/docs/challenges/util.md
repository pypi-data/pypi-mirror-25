Util
====

Utility Functions for Challenges

This module defines useful and frequently used functions for use in Challenges.
Import this module to use them.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
--------------

### get_element_image(element, browser)

Takes a screenshot and crops out the element

**Args:**

|  Name   |    Type    |      Description       |
|---------|------------|------------------------|
| element | Webelement | The element to crop    |
| browser | Browser    | The web browser to use |

**Returns:**

|  Type  |         Description         |
|--------|-----------------------------|
| Object | A base64 encoded JPEG image |


### get_image_from_swf(url, timeout)

Takes a screenshot of a Flash object (.swf)

**Args:**

|  Name   |  Type   |                       Description                       |
|---------|---------|---------------------------------------------------------|
| url     | String  | The URL of the SWF                                      |
| timeout | Integer | The length of time to wait before taking the screenshot |

**Returns:**

|  Type  |         Description         |
|--------|-----------------------------|
| Object | A base64 encoded JPEG image |


### get_image_src(element)

Downloads the source of an image

**Args:**

|  Name   |    Type    |       Description       |
|---------|------------|-------------------------|
| element | Webelement | The element to download |

**Returns:**

|  Type  |      Description       |
|--------|------------------------|
| Object | A base64 encoded image |
