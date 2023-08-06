

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Pay follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Pay uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.pay.png
  :target: https://travis-ci.org/OneGov/onegov.pay
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.pay/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.pay?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.pay.svg
    :target: https://badge.fury.io/py/onegov.pay
    :alt: Latest PyPI Release

License
-------
onegov.pay is released under GPLv2

Changelog
---------

0.3.0 (2017-10-10)
~~~~~~~~~~~~~~~~~~~~~

- Adds proper support for many-to-many payments.
  [href]

0.2.0 (2017-10-06)
~~~~~~~~~~~~~~~~~~~~~

- Adds a helper method to get the association table for a given Payable.
  [href]

- Switch to onegov.core's generic association implementation.
  [href]

0.1.1 (2017-07-05)
~~~~~~~~~~~~~~~~~~~~~

- Fixes Stripe payment syncing failing if there was a payout.
  [href]

0.1.0 (2017-06-16)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release


