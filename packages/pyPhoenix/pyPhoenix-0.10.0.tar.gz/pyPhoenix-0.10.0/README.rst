Phoenix database adapter for Python
===================================

``pyphoenix`` is a Python library for accessing the
`Phoenix SQL database <http://phoenix.apache.org/>`_
using the
`remote query server <http://phoenix.apache.org/server.html>`_ introduced
in Phoenix 4.4.  The library implements the  
standard `DB API 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ interface,
which should be familiar to most Python programmers.
It include sqlachemy plugins.


Installation
------------

The easiest way to install the library is using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install pyPhoenix

You can also download the source code and install it manually::

    cd /path/to/pyphoenix/
    python setup.py install

Usage
-----

The library implements the standard DB API 2.0 interface, so it can be
used the same way you would use any other SQL database from Python, for example::

    import pyphoenix

    database_url = 'http://localhost:8765/'
    conn = pyphoenix.connect(database_url, autocommit=True)

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR)")
    cursor.execute("UPSERT INTO users VALUES (?, ?)", (1, 'admin'))
    cursor.execute("SELECT * FROM users")
    print cursor.fetchall()

Phoenix versions
----------------

Phoenix 4.7 uses a serialization based on Protocol Buffers (proto3) by default.

This library only supports Protocol serialization.

Setting up a development environment
------------------------------------

If you want to quickly try out the included examples, you can set up a
local `virtualenv <https://virtualenv.pypa.io/en/latest/>`_ with all the
necessary requirements::

    virtualenv e
    source e/bin/activate
    pip install -r requirements.txt
    python setup.py develop

If you need a Phoenix server for experimenting, you can get one running
quickly using Vagrant::

    vagrant up

You can connect to the virtual machine and work with the Phoenix shell
from there::

    vagrant ssh
    /opt/phoenix/bin/sqlline.py localhost

Interactive SQL shell
---------------------

There is a Python-based interactive shell include in the examples folder, which can be
used to connect to Phoenix and execute queries::

    ./examples/shell.py http://localhost:8765/
    db=> CREATE TABLE test (id INTEGER PRIMARY KEY, name VARCHAR);
    no rows affected (1.363 seconds)
    db=> UPSERT INTO test (id, name) VALUES (1, 'Lukas');
    1 row affected (0.004 seconds)
    db=> SELECT * FROM test;
    +------+-------+
    |   ID | NAME  |
    +======+=======+
    |    1 | Lukas |
    +------+-------+
    1 row selected (0.019 seconds)

Running the test suite
----------------------

The library comes with a test suite for testing Python DB API 2.0 compliance and
various Phoenix-specific features. In order to run the test suite, you need a
working Phoenix database and set the ``pyphoenix_TEST_DB_URL`` environment variable::

    export pyphoenix_TEST_DB_URL='http://localhost:8765/'
    nosetests

Known issues
------------

- In general, the library has not been battle-tested yet. You might encounter almost any problem. Use with care.
- You can only use the library in autocommit mode. The native Java Phoenix library also implements batched upserts, which can be committed at once, but this is not exposed over the remote server.
  (`CALCITE-767 <https://issues.apache.org/jira/browse/CALCITE-767>`_)
- TIME and DATE columns in Phoenix are stored as full timestamps with a millisecond accuracy,
  but the remote protocol only exposes the time (hour/minute/second) or date (year/month/day)
  parts of the columns. (`CALCITE-797 <https://issues.apache.org/jira/browse/CALCITE-797>`_, `CALCITE-798 <https://issues.apache.org/jira/browse/CALCITE-798>`_)
- TIMESTAMP columns in Phoenix are stored with a nanosecond accuracy, but the remote protocol truncates them to milliseconds. (`CALCITE-796 <https://issues.apache.org/jira/browse/CALCITE-796>`_)
- ARRAY columns are not supported.
  (`CALCITE-1050 <https://issues.apache.org/jira/browse/CALCITE-1050>`_, `PHOENIX-2585 <https://issues.apache.org/jira/browse/PHOENIX-2585>`_)

SQLachemy
===================================
- Creates versions for select
- select over queryserver with pyphoenix

Usage
-----

example::

    import sqlalchemy

    db = sqlalchemy.create_engine('phoenix://localhost:8765/')
    conn = db.connect()

