ruCaptcha
=========

ruCaptcha Library

The ruCaptcha library defines functions to interact with ruCaptcha's web API.
See the unit tests for this library for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Functions:**
--------------

#### post_image(key, image)

Posts an image to be solved

**Args:**

| Name  |  Type  |           Description            |
|-------|--------|----------------------------------|
| key   | String | The API key to use               |
| image | Bytes  | The base64 encoded image to post |

**Returns:**

|  Type  |        Description         |
|--------|----------------------------|
| String | The ID of the posted image |

**Raises:**

|     Name     |   Description   |
|--------------|-----------------|
| RuntimeError | The post failed |

#### post_image_grid(key, image, text, rows, columns)

Posts an image grid to be solved

**Args:**

|  Name   |  Type   |           Description            |
|---------|---------|----------------------------------|
| key     | String  | The API key to use               |
| image   | Bytes   | The base64 encoded image to post |
| text    | String  | The instructions for the image   |
| rows    | Integer | The number of rows               |
| columns | Integer | The number of columns            |

**Returns:**

|  Type  |        Description         |
|--------|----------------------------|
| String | The ID of the posted image |

**Raises:**

|     Name     |   Description   |
|--------------|-----------------|
| RuntimeError | The post failed |

#### get(key, id)

Gets the result of a posted image

**Args:**

| Name |  Type  |        Description         |
|------|--------|----------------------------|
| key  | String | The API key to use         |
| id   | String | The ID of the posted image |

**Returns:**

|  Type  |          Description           |
|--------|--------------------------------|
| String | The result of the posted image |

**Raises:**

|     Name     |  Description   |
|--------------|----------------|
| RuntimeError | The get failed |

#### invalid(key, id)

Reports a posted image as invalid

**Args:**

| Name |  Type  |        Description         |
|------|--------|----------------------------|
| key  | String | The API key to use         |
| id   | String | The ID of the posted image |

#### get_rate(currency, rate = 0.0)

Calculates the solving rate in any currency

**Args:**

|   Name   |  Type  |        Description         |
|----------|--------|----------------------------|
| currency | String | The currency to convert to |
| rate     | Float  | A constant solving rate    |

**Returns:**

| Type  |                 Description                 |
|-------|---------------------------------------------|
| Float | The solving rate as a floating point number |

The currency must be a three letter code like USD or EUR. If `rate` is set,
it will override the rate received from ruCaptcha's API.

#### scale_image(image)

Scales a base64 encoded image to meet ruCaptcha's requirements

**Args:**

| Name  | Type  |       Description        |
|-------|-------|--------------------------|
| image | Bytes | The base64 encoded image |

**Returns:**

| Type  |         Description         |
|-------|-----------------------------|
| Bytes | A base64 encoded JPEG image |
