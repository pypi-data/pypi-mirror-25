Web
===

Web Interfaces

This module defines objects for interacting with the World Wide Web. See the
documentation for each object and their respective unit tests for more
information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Browser(object)

A web browser

**Args:**

| Name  |  Type  |   Description    |
|-------|--------|------------------|
| proxy | String | The proxy to use |

**Raises:**

|    Type    |     Description      |
|------------|----------------------|
| ValueError | The proxy is invalid |

Browser is a wrapper for the web browser automation tool Selenium. To
simplify things and to avoid linking to external binaries, only Firefox
is supported. Firefox natively supports Selenium without any configuration.

A proxy may be used and must be in the form of `host:port`. The host
can be a fully qualified domain name (FQDN) or an IP address. The port
must be a valid integer. You may also set the proxy to None for no proxy.

Example:

	127.0.0.1:3128
	localhost:3128
	None

#### action()

Creates an ActionChains object to string together operations

**Returns:**

|  Type  |      Description       |
|--------|------------------------|
| Object | An ActionChains object |

An action chain is useful for doing complex actions like hover over
and drag and drop. This function returns an ActionChains object with
the Browser passed as an argument and can be used just like the
original found here:

http://selenium-python.readthedocs.io/api.html

#### get(url)

Requests a URL in the browser

**Args:**

| Name |  Type  |    Description     |
|------|--------|--------------------|
| url  | String | The URL to request |

If the page load time exceeds the default timeout limit, it will
automatically be handled by forcing the Browser to stop loading.
You can set the default timeout with the `set_timeout()` function.

#### set_timeout(time)

Changes the length of time a page is allowed to load before it stops

**Args:**

| Name |  Type   |          Description          |
|------|---------|-------------------------------|
| time | Integer | The page load time in seconds |

**Raises:**

|    Type    |          Description          |
|------------|-------------------------------|
| ValueError | The page load time is invalid |
