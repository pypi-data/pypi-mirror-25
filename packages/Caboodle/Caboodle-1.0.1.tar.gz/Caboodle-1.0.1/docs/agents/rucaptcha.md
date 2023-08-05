Rucaptcha
=========

ruCaptcha Challenge solving Agents

This module is an implementation of the Agent specification and solves a
Challenge using the paid online service ruCaptcha. To use these Agents, create a
new instance of one and call the `solve()` function. See the documentation for
each Agent and their respective unit tests for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### RucaptchaImageAgent(caboodle.agents.spec.Agent)

An Agent to solve image based Challenges using ruCaptcha

**Args:**

|   Name   |  Type  |          Description          |
|----------|--------|-------------------------------|
| key      | String | The API key to use            |
| currency | String | The currency to calculate for |

The currency must be a three letter code like USD or EUR.

#### fail(data)

Performs actions for a failed Challenge

**Args:**

| Name |    Type    |     Description      |
|------|------------|----------------------|
| data | Dictionary | The failed Challenge |

#### get_cost()

Returns the cost of using this Agent

**Returns:**

|  Type   |             Description             |
|---------|-------------------------------------|
| Integer | The cost as a floating point number |

#### solve(data)

Solves a Challenge and stores the result

**Args:**

| Name |    Type    |      Description       |
|------|------------|------------------------|
| data | Dictionary | The Challenge to solve |

**Raises:**

|   Type    |            Description            |
|-----------|-----------------------------------|
| TypeError | The Challenge is not a dictionary |

#### success(data)

Performs actions for a successful Challenge

**Args:**

| Name |    Type    |       Description        |
|------|------------|--------------------------|
| data | Dictionary | The successful Challenge |


### RucaptchaImageGridAgent(caboodle.agents.spec.Agent)

An Agent to solve image grid based Challenges using ruCaptcha

**Args:**

|   Name   |  Type  |          Description          |
|----------|--------|-------------------------------|
| key      | String | The API key to use            |
| currency | String | The currency to calculate for |

The currency must be a three letter code like USD or EUR.

#### fail(data)

Performs actions for a failed Challenge

**Args:**

| Name |    Type    |     Description      |
|------|------------|----------------------|
| data | Dictionary | The failed Challenge |

#### get_cost()

Returns the cost of using this Agent

**Returns:**

|  Type   |             Description             |
|---------|-------------------------------------|
| Integer | The cost as a floating point number |

#### solve(data)

Solves a Challenge and stores the result

**Args:**

| Name |    Type    |      Description       |
|------|------------|------------------------|
| data | Dictionary | The Challenge to solve |

**Raises:**

|   Type    |            Description            |
|-----------|-----------------------------------|
| TypeError | The Challenge is not a dictionary |

#### success(data)

Performs actions for a successful Challenge

**Args:**

| Name |    Type    |       Description        |
|------|------------|--------------------------|
| data | Dictionary | The successful Challenge |
