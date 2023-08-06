===========
Certifiable
===========

.. image:: https://img.shields.io/badge/Author:%20francis%20horsman-Available-brightgreen.svg?style=plastic
    :target: https://www.linkedin.com/in/francishorsman

.. image:: https://img.shields.io/pypi/v/certifiable.svg
    :target: https://pypi.python.org/pypi/certifiable
        :alt: PyPi version

.. image:: https://img.shields.io/travis/sys-git/certifiable.svg
    :target: https://travis-ci.org/sys-git/certifiable
        :alt: CI Status

.. image:: https://coveralls.io/repos/github/sys-git/certifiable/badge.svg
    :target: https://coveralls.io/github/sys-git/certifiable
        :alt: Coverage Status

.. image:: https://badge.fury.io/py/certifiable.svg
    :target: https://badge.fury.io/py/certifiable

.. image:: https://img.shields.io/pypi/l/certifiable.svg
    :target: https://img.shields.io/pypi/l/certifiable.svg

.. image:: https://img.shields.io/pypi/wheel/certifiable.svg
    :target: https://img.shields.io/pypi/wheel/certifiable.svg

.. image:: https://img.shields.io/pypi/pyversions/certifiable.svg
    :target: https://img.shields.io/pypi/pyversions/certifiable.svg

.. image:: https://img.shields.io/pypi/status/certifiable.svg
    :target: https://img.shields.io/pypi/status/certifiable.svg

.. image:: https://readthedocs.org/projects/certifiable/badge/?version=latest
    :target: https://certifiable.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sys-git/certifiable/shield.svg
    :target: https://pyup.io/repos/github/sys-git/certifiable/
    :alt: Updates

Certifiable is a powerful runtime parameter validation library for python.

Features
--------

Examples of all features can be found here: :ref:`usage`.

It can validate the following *basic* types:

* Text
* Unicode
* String
* Bytes
* Bool
* Int
* Long
* Number
* Decimal
* Float
* Enum
* Timestamp
* Date
* Object


And also these more `complex` or compound types into which you can pass `other` certifiers:

* List
* Tuple
* Set
* Iterable
* Dict
* Json
* Html
* Email

There are logical operators to combine certifiers:

* ANY   (certify_only_one)
* AND   (certify_all)
* ALL   (certify_all)
* NAND  (certify_none)
* XOR   (certify_only_one)


Status
------

ALPHA

* Free software: MIT license
* Documentation: https://certifiable.readthedocs.io.
