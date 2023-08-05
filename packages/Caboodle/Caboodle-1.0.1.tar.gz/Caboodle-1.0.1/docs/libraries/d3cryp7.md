d3cryp7
=======

d3cryp7 Library

The d3cryp7 library defines functions to interact with d3cryp7's web API.
See the unit tests for this library for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
--------------

#### recognize_image(url, image)

Posts an image to be recognized

**Args:**

| Name  |  Type  |           Description            |
|-------|--------|----------------------------------|
| url   | String | The URL of the d3cryp7 API       |
| image | Bytes  | The base64 encoded image to post |

**Returns:**

|  Type  |               Description                 |
|--------|-------------------------------------------|
| String | A string containing the text in the image |

**Raises:**

|     Name     |   Description   |
|--------------|-----------------|
| RuntimeError | The post failed |

#### tag_image(url, image)

Posts an image to be tagged

**Args:**

| Name  |  Type  |           Description            |
|-------|--------|----------------------------------|
| url   | String | The URL of the d3cryp7 API       |
| image | Bytes  | The base64 encoded image to post |

**Returns:**

|    Type    |                 Description                  |
|------------|----------------------------------------------|
| Dictionary | A dictionary of tags and their probabilities |

**Raises:**

|     Name     |   Description   |
|--------------|-----------------|
| RuntimeError | The post failed |

#### tag_image_grid(url, image, col, row)

Posts an image grid to be tagged

**Args:**

| Name  |  Type   |            Description             |
|-------|---------|------------------------------------|
| url   | String  | The URL of the d3cryp7 API         |
| image | Bytes   | The base64 encoded image to post   |
| col   | Integer | The number of columns in the image |
| row   | Integer | The number of rows in the image    |

**Returns:**

| Type  |                      Description                        |
|-------|---------------------------------------------------------|
| Tuple | A tuple of dictionaries of tags and their probabilities |

**Raises:**

|     Name     |   Description   |
|--------------|-----------------|
| RuntimeError | The post failed |

#### generate_bbs(w, h, col, row)

Generates a tuple of bounding boxes to crop a grid of images

**Args:**

| Name |  Type   |            Description            |
|---- -|---------|-----------------------------------|
| w    | Integer | The width of an image             |
| h    | Integer | The height of an image            |
| col  | Integer | The number of columns in an image |
| row  | Integer | The number of rows in an image    |

**Returns:**

| Type  |                Description                |
|-------|-------------------------------------------|
| Tuple | A tuple of tuples that contain 4 integers |

#### get_rate(url, currency)

Calculates the solving rate in any currency

**Args:**

|   Name   |  Type  |        Description         |
|----------|--------|----------------------------|
| url      | String | The URL of the d3cryp7 API |
| currency | String | The currency to convert to |

**Returns:**

|    Type    |                       Description                       |
|------------|---------------------------------------------------------|
| Dictionary | A dictionary of solving rates as floating point numbers |

The currency must be a three letter code like USD or EUR.

#### success(url, id)

Reports a posted image as successful

**Args:**

| Name |  Type  |        Description         |
|------|--------|----------------------------|
| url  | String | The URL of the d3cryp7 API |
| id   | String | The ID of the posted image |

#### invalid(url, id)

Reports a posted image as invalid

**Args:**

| Name |  Type  |        Description         |
|------|--------|----------------------------|
| url  | String | The URL of the d3cryp7 API |
| id   | String | The ID of the posted image |
