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

Certifiable is a powerful runtime parameter validation library for python, see: :ref:`usage`.

Use it in in conjunction with `HOFT <http://hoft.readthedocs.io/en/latest/>`_ to automatically
validate method args and kwargs.

Example::

    >>> from certifiable import certify_bool
    >>> certify_bool(True)
    >>> certify_bool(False)
    >>> certify_bool('hello world')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/certifiable.py", line 63, in wrapper
        certify(value)
      File "certifiable/certifiable.py", line 60, in certify
        func(value, **kwargs)
      File "certifiable/certifiable.py", line 512, in certify_bool
        required=required,
    certifiable.errors.CertifierTypeError: expected bool, but value is of type 'str'
    >>>



Contents:

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   contributing
   authors
   history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
