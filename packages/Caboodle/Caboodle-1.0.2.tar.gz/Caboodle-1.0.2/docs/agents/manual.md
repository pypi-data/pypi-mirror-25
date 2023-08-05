Manual
======

A manually defined Challenge solving Agent

This module is an implementation of the Agent specification and solves a
Challenge using an external function defined by the user. To use this Agent,
create a new instance of it with the desired solving function and call the
`solve()` function. See the unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### ManualAgent(caboodle.agents.spec.Agent)

An Agent to solve Challenges with external functions

**Args:**

|       Name       |   Type   |             Description             |
|------------------|----------|-------------------------------------|
| solve_function   | Function | The function to solve the Challenge |
| success_function | Function | The function called on success      |
| fail_function    | Function | The function called on fail         |

**Raises:**

|   Type    |          Description          |
|-----------|-------------------------------|
| TypeError | An argument is not a function |

This Agent will, by default, have a cost of zero. As a general guideline,
the solving function should append the result to the dictionary with the
key 'result'.

Example:

	lambda data: data.update({'result': 42})

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

|     Type     |                   Description                    |
|--------------|--------------------------------------------------|
| TypeError    | The Challenge is not a dictionary                |
| ValueError   | The Challenge does not contain the required data |
| RuntimeError | The Challenge could not be solved                |

#### success(data)

Performs actions for a successful Challenge

**Args:**

| Name |    Type    |       Description        |
|------|------------|--------------------------|
| data | Dictionary | The successful Challenge |
