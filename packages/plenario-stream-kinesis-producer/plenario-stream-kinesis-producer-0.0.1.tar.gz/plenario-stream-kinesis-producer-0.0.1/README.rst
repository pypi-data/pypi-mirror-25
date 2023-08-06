Plenario Stream Kinesis Producer
================================

This project provides listeners which convert jobs managed by plenario
into messages on a Kinesis stream.


|Build Status|
|Code Coverage|


Requirements
------------

Python3.6_, PostgreSQL_

.. _Python3.6: https://www.python.org/downloads/release/python-362/
.. _PostgreSQL: https://www.postgresql.org/download/


Setup
-----

Install python dependencies

.. code:: python

   pip install -r requirements-dev.txt

Ensure your cache and database services are running

.. code:: bash

   service postgresql status


Test
----

.. code:: bash

    ./manage.py test

.. |Build Status| image:: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-kinesis-producer.svg
    :target: https://travis-ci.org/UrbanCCD-UChicago/plenario-stream-kinesis-producer
.. |Code Coverage| image:: https://coveralls.io/repos/github/UrbanCCD-UChicago/plenario-stream-kinesis-producer/badge.svg
    :target: https://coveralls.io/github/UrbanCCD-UChicago/plenario-stream-kinesis-producer