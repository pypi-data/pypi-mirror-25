jsontableschema-sql-py
======================

| |Travis|
| |Coveralls|
| |PyPi|
| |SemVer|
| |Gitter|

Generate and load SQL tables based on JSON Table Schema descriptors.

    Version ``v0.3`` contains breaking changes:

-  renamed ``Storage.tables`` to ``Storage.buckets``
-  changed ``Storage.read`` to read into memory
-  added ``Storage.iter`` to yield row by row

Getting Started
---------------

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install tableschema-sql

Storage
~~~~~~~

Package implements `Tabular
Storage <https://github.com/frictionlessdata/jsontableschema-py#storage>`__
interface.

SQLAlchemy is used as sql wrapper. We can get storage this way:

.. code:: python

    from sqlalchemy import create_engine
    from tableschema_sql import Storage

    engine = create_engine('sqlite:///:memory:', prefix='prefix')
    storage = Storage(engine)

Then we could interact with storage:

.. code:: python

    storage.buckets
    storage.create('bucket', descriptor)
    storage.delete('bucket')
    storage.describe('bucket') # return descriptor
    storage.iter('bucket') # yield rows
    storage.read('bucket') # return rows
    storage.write('bucket', rows)

Mappings
~~~~~~~~

::

    schema.json -> SQL table schema
    data.csv -> SQL talbe data

Drivers
~~~~~~~

SQLAlchemy is used - `docs <http://www.sqlalchemy.org/>`__.

API Reference
-------------

Snapshot
~~~~~~~~

https://github.com/frictionlessdata/jsontableschema-py#snapshot

Detailed
~~~~~~~~

-  `Docstrings <https://github.com/frictionlessdata/jsontableschema-py/tree/master/jsontableschema/storage.py>`__
-  `Changelog <https://github.com/frictionlessdata/jsontableschema-sql-py/commits/master>`__

Contributing
------------

Please read the contribution guideline:

`How to Contribute <CONTRIBUTING.md>`__

Thanks!

.. |Travis| image:: https://img.shields.io/travis/frictionlessdata/jsontableschema-sql-py/master.svg
   :target: https://travis-ci.org/frictionlessdata/jsontableschema-sql-py
.. |Coveralls| image:: http://img.shields.io/coveralls/frictionlessdata/jsontableschema-sql-py/master.svg
   :target: https://coveralls.io/r/frictionlessdata/jsontableschema-sql-py?branch=master
.. |PyPi| image:: https://img.shields.io/pypi/v/jsontableschema-sql.svg
   :target: https://pypi.python.org/pypi/jsontableschema-sql
.. |SemVer| image:: https://img.shields.io/badge/versions-SemVer-brightgreen.svg
   :target: http://semver.org/
.. |Gitter| image:: https://img.shields.io/gitter/room/frictionlessdata/chat.svg
   :target: https://gitter.im/frictionlessdata/chat

