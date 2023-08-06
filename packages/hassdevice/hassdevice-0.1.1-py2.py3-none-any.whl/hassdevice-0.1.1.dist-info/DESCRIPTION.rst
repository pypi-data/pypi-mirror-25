========
Overview
========



A library for building MQTT devices for HomeAssistant

* Free software: Apache Software License 2.0

Installation
============

::

    pip install hassdevice

Documentation
=============

https://python-hassdevice.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.0.2 (2017-07-17)
------------------

* Drop Python 2.7 support
* Add `hassdevice.hosts.SimpleMQTTHost`

0.0.1 (2017-07-10)
------------------

* First release on PyPI.


