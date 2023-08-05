Spec
====

Specifications for Challenge solving agents

This module defines abstract classes with compounding levels of functionality.
Every Agent should have a `solve()` and `get_cost()` function and, by default,
will initialize the cost of the Agent to zero. These specifications can not be
instantiated and can only be used by a subclass that implements all of the
required functions. Be sure, however, to explicitly call the `super()` function
from each subclass and from each defined function in that subclass to gain the
functionality of it's parent. See the unit tests for this module for more
information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Agent(object)

An agent to solve Challenges

An Agent processes data from a Challenge in the form of a dictionary to
produce a result. This result is added to the dictionary if and when it
succeeds. As a general guideline, the result should be appended to the
dictionary with the key 'result'.

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
