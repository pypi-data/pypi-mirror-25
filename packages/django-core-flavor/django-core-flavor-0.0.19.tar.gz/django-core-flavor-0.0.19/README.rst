Django Core Flavor
==================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

A Django application that provides core tools

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.10

Installation
------------

Install last stable version from pypi.

.. code:: sh

    pip install django-core-flavor

Add ``core_flavor`` to your INSTALLED_APPS setting.

.. code:: python

    INSTALLED_APPS = (
        ...
        'core_flavor.apps.CoreAppConfig',
    )

.. |Pypi| image:: https://img.shields.io/pypi/v/django-core-flavor.svg
   :target: https://pypi.python.org/pypi/django-core-flavor

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-core-flavor.svg
   :target: https://pypi.python.org/pypi/django-core-flavor

.. |Build Status| image:: https://travis-ci.org/flavors/core.svg?branch=master
   :target: https://travis-ci.org/flavors/core

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/core.svg
   :target: https://codecov.io/gh/flavors/core

.. |Code Climate| image:: https://codeclimate.com/github/flavors/core/badges/gpa.svg
   :target: https://codeclimate.com/github/flavors/core
