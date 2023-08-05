Solve
=====

Challenge Solving Utilities

This module uses Agents to solve Challenges. Both are modular and any number of
them can be added. A Solver works by running every loaded Challenge and checking
if it returned any data. If it did, then every Solver is ran from least cost to
greatest until a result is found or a RuntimeError is raised indicating that the
Challenge could not be solved. Because of the way the Solver works, it is
imperative that every Challenge and Agent operate according to their
specifications. See the unit tests for this module for more information.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

**Classes:**
------------

### Solver(object)

Solves challenges in a Browser

**Args:**

|  Name   |  Type   |      Description       |
|---------|---------|------------------------|
| browser | Browser | The web browser to use |

**Raises:**

|   Type    |            Description             |
|-----------|------------------------------------|
| TypeError | The browser is not of type Browser |

#### add_agent(agent)

Adds an Agent to the list of available solving agents

**Args:**

| Name  | Type  |   Description    |
|-------|-------|------------------|
| agent | Agent | The Agent to add |

**Raises:**

|   Type    |          Description           |
|-----------|--------------------------------|
| TypeError | The agent is not of type Agent |

#### add_challenge(challenge)

Adds a Challenge to the list of challenge types

**Args:**

|   Name    |   Type    |     Description      |
|-----------|-----------|----------------------|
| challenge | Challenge | The Challenge to add |

**Raises:**

|   Type    |              Description               |
|-----------|----------------------------------------|
| TypeError | The challenge is not of type Challenge |

#### set_fail(id)

Sets a Challenge as failed and handles it appropriately before removing
it from the list

**Args:**

| Name |  Type  |       Description       |
|------|--------|-------------------------|
| id   | String | The ID of the Challenge |

**Raises:**

|   Type   |     Description      |
|----------|----------------------|
| KeyError | The ID was not found |

#### set_success(id)

Sets a Challenge as successful and handles it appropriately before
removing it from the list

**Args:**

| Name |  Type  |       Description       |
|------|--------|-------------------------|
| id   | String | The ID of the Challenge |

**Raises:**

|   Type   |     Description      |
|----------|----------------------|
| KeyError | The ID was not found |

#### solve()

Solves a Challenge

**Returns:**

|  Type  |       Description       |
|--------|-------------------------|
| Object | The ID of the Challenge |

**Raises:**

|     Type     |            Description            |
|--------------|-----------------------------------|
| RuntimeError | The Challenge could not be solved |
