Plenario Stream Core
====================


|Build Status|
|Code Coverage|


Requirements
------------

Python3.6_, Redis_, PostgreSQL_

.. _Python3.6: https://www.python.org/downloads/release/python-362/
.. _Redis: https://redis.io/download
.. _PostgreSQL: https://www.postgresql.org/download/


Setup
-----

Install python dependencies

.. code:: python

   pip install -r requirements-dev.txt

Ensure your cache and database services are running

.. code:: bash

   service redis status
   service postgresql status

Run migrations

.. code:: bash

    ./manage.py migrate

Run
---

bash
''''

.. code:: bash

    ./manage.py runserver

Test
----

.. code:: bash

    ./manage.py test

.. |Build Status| image:: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-core.svg
    :target: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-core
.. |Code Coverage| image:: https://coveralls.io/repos/github/UrbanCCD-UChicago/plenario-stream-core/badge.svg
    :target: https://coveralls.io/github/UrbanCCD-UChicago/plenario-stream-core
