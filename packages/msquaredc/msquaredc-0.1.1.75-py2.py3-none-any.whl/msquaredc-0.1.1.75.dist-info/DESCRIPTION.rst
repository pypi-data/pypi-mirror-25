========
Overview
========

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :alt: Donate
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=RUTXGLRTZ9YQ8
.. image:: http://badges.gitter.im/j340m3/msquaredc.svg
    :alt: Join the chat at https://gitter.im/msquaredc/Lobby
    :target: https://gitter.im/msquaredc/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge



An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD license

Installation
============

::

    pip install msquaredc

Documentation
=============

https://python-msquaredc.readthedocs.io/

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

Donation
========
Please consider to support me:

.. image:: http://www.wenspencer.com/wp-content/uploads/2017/02/patreon-button.png
    :alt: Become a patron
    :target: https://patreon.com/j340m3


Changelog
=========

0.1.0 (2017-04-18)
------------------

* First release on PyPI.


