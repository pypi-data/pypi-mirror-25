Caboodle Wiki
=============

Caboodle is a Python module for web browsing, web scraping or web automation
developed to provide an all-in-one (kit and caboodle) utility for anything the
web has to offer.

> [kuh-bood-l] **noun**, *Informal*
>
> 1. the lot, pack, or crowd

Install
-------

	pip install caboodle

What's New
----------

Caboodle v1 has been redesigned from scratch to be more modular and to allow
new features to be easily added by using a simple API.

The Solver has been divided into two classes, Challenges and Agents.

A Challenge is simply an object that collects data from the current web page and
returns it as a dictionary that can then be processed by an Agent.

An Agent, on the other hand, does all the hard work and is basically an
interface to another application. An Agent will process all the collected data
and return a result if it succeeds.

The whole process is called *"solving"*. When you create a Solver and call the
`solve()` function, every loaded Challenge is called to attempt to
collect data. If and when a Challenge collects data, that data is then sent to
every loaded Agent to attempt to solve it. If a solution is found, it is added
to the data and then sent back to the Challenge to be used. Otherwise, an
exception is raised because no solution was found.

If you don't get a solution, you could try to create a manual implementation
using either the Manual Challenge or the Manual Agent. If it works for you,
perhaps you could contribute it to the project in a pull request.

The whole of this project is dead simple; connecting parts to other parts. It
shouldn't be complicated and that is what the redesign for v1 aimed to do.

Examples
--------

Examples have been removed for now and will be created again once v1 is
officially released. For now, read through the [documentation] and the
[unit tests], and consult the `help()` function if you need help.

Resources
---------

[Selenium Documentation]

[Segmenting letters in a CAPTCHA image]

[documentation]: https://bitbucket.org/bkvaluemeal/caboodle/src/future/docs
[unit tests]: https://bitbucket.org/bkvaluemeal/caboodle/src/future/tests
[Selenium Documentation]: http://selenium-python.readthedocs.io
[Segmenting letters in a CAPTCHA image]: http://stackoverflow.com/questions/33294595/segmenting-letters-in-a-captcha-image
