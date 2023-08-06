=====
Crash
=====

.. image:: https://travis-ci.org/crate/crash.svg?branch=master
    :target: https://travis-ci.org/crate/crash
    :alt: Travis CI

.. image:: https://badge.fury.io/py/crash.png
    :target: http://badge.fury.io/py/crash
    :alt: Version

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://crate.io/docs/reference/crash/
    :alt: Documentation

.. image:: https://img.shields.io/pypi/pyversions/crash.svg
    :target: https://pypi.python.org/pypi/crash/
    :alt: Python Version

.. image:: https://img.shields.io/coveralls/crate/crash.svg
    :target: https://coveralls.io/r/crate/crash?branch=master
    :alt: Coverage

|

Crash is an interactive CrateDB *command line interface* (CLI) SQL shell with autocompletion.

Screenshot
==========

.. image:: crash.png
    :alt: A screenshot of Crash

Prerequisites
=============

Recent versions of Crash require Python (>= 2.7) to run.

Use Crash 0.16.0 if you're running Python 2.6.

Installation
============

As a Python Package
-------------------

Crash is available as a pip_ package.

To install, run::

    $ pip install crash

Now, run it::

    $ crash

To update, run::

    $ pip install -U crash

Standalone
----------

Crash is also available as a standalone executable that includes all the
necessary dependencies, and can be run as long as Python (>= 2.7) is available.

First, download the executable::

    $ curl -o crash https://cdn.crate.io/downloads/releases/crash_standalone_latest

Then, make it executable::

    $ chmod +x crash

Now, run it::

    $ ./crash

If you would like to run ``crash`` from any directory and without using leading
``./`` you will need to move it to somewhere on your ``$PATH``.

Usage
=====

For usage information and options, run::

    $ crash --help

Contributing
============

This project is primarily maintained by Crate.io_, but we welcome community
contributions!

See the `developer docs`_ and the `contribution docs`_ for more information.

Help
====

Looking for more help?

- Read `the project documentation`_
- Check `StackOverflow`_ for common problems
- Chat with us on `Slack`_
- Get `paid support`_

.. _contribution docs: CONTRIBUTING.rst
.. _Crate.io: http://crate.io/
.. _developer docs: DEVELOP.rst
.. _paid support: https://crate.io/pricing/
.. _pip: https://pypi.python.org/pypi/pip
.. _Slack: https://crate.io/docs/support/slackin/
.. _StackOverflow: https://stackoverflow.com/tags/crate
.. _the project documentation: https://crate.io/docs/reference/crash/

====================
Installation & Usage
====================

If the package was installed using ``pip`` the shell can be started by
invoking ``crash`` in a terminal. We recommend to install it to the Python
user install directory to avoid unwanted dependency conflicts.

::

    pip install --user crash


.. note::
    If ``crash`` is installed in the Python user install directory please ensure
    that ``~/.local/bin`` (Linux), or ``%APPDATA%\Python\<version>\Scripts``
    (Windows) is added to the system path.

``crash`` by default will try to connect to ``localhost:4200``. To connect to
another host use the ``connect`` command inside the shell or use the ``--hosts``
argument when launching the shell.

``crash`` started with the ``-v`` switch (once or more times) will log useful information
when it comes to debugging, like what connection attempts are made and full tracebacks
of server errors.

For more information about the available command line arguments see `Command Line Arguments`_.

When you connect to a server that is not reachable or whose hostname cannot be resolved
you will get an error::

    cr> \connect 127.0.0.1:65535
    +------------------------+-----------+---------+-----------+-----------...-+
    | server_url             | node_name | version | connected | message       |
    +------------------------+-----------+---------+-----------+-----------...-+
    | http://127.0.0.1:65535 |      NULL | 0.0.0   | FALSE     | Server not... |
    +------------------------+-----------+---------+-----------+-----------...-+
    CONNECT ERROR

::

    cr> \connect 300.300.300.300:4200
    +-----------------------------+-----------+---------+-----------+-------------...-+
    | server_url                  | node_name | version | connected | message         |
    +-----------------------------+-----------+---------+-----------+-------------...-+
    | http://300.300.300.300:4200 |      NULL | 0.0.0   | FALSE     | Server not a... |
    +-----------------------------+-----------+---------+-----------+-------------...-+
    CONNECT ERROR

Successful connects will give you some information about the servers you connect to::

    cr> \connect 127.0.0.1:44209;
    +------------------------+-----------+---------+-----------+---------+
    | server_url             | node_name | version | connected | message |
    +------------------------+-----------+---------+-----------+---------+
    | http://127.0.0.1:44209 | crate     | ...     | TRUE      | OK      |
    +------------------------+-----------+---------+-----------+---------+
    CONNECT OK...

If you connect to more than one server, the command will succeed
if at least one server is reachable::

    cr> \connect 127.0.0.1:44209 300.300.300.300:4295;
    +-----------------------------+-----------+---------+-----------+-----------...-+
    | server_url                  | node_name | version | connected | message       |
    +-----------------------------+-----------+---------+-----------+-----------...-+
    | http://127.0.0.1:44209      | crate     | ...     | TRUE      | OK            |
    | http://300.300.300.300:4295 | NULL      | 0.0.0   | FALSE     | Server not... |
    +-----------------------------+-----------+---------+-----------+-----------...-+
    CONNECT OK...

Once the shell is connected, SQL statements can be executed simply by entering
them without any special arguments like this::

    cr> SELECT table_name FROM information_schema.tables
    ... WHERE table_name = 'cluster';
    +------------+
    | table_name |
    +------------+
    | cluster    |
    +------------+
    SELECT 1 row in set (... sec)

When the CrateDB shell is started with the option ``-v`` debugging information will be printed::

    cr> select x from y;
    SQLActionException[TableUnknownException: Table 'doc.y' unknown]
    SQLActionException: NOT_FOUND 4041 TableUnknownException: Table 'doc.y' unknown
    ...


Limitations
===========

.. note::

    Due to changes in the Information Schema of CrateDB, Crash versions <= 0.19
    are not compatible with CrateDB > 0.57.

Nested Objects and Arrays
-------------------------

.. note::

    Since CrateDB 0.39.0 it is possible to use object and array literals and the
    limitation does not apply when connecting to a CrateDB instance running > 0.39.0.

While it is possible to select or filter by nested objects it is currently not
possible to insert them using Crash. In order to do that the `CrateDB REST
endpoint`_ or a client library like `crate-python`_ has to be used.

The same also applies for arrays.

.. _`CrateDB REST Endpoint`: https://crate.io/docs/current/sql/rest.html
.. _`Command Line Arguments`: https://crate.io/docs/projects/crash/en/stable/cli.html
.. _`crate-python`: https://pypi.python.org/pypi/crate/


