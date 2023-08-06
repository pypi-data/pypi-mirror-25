#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

__all__ = [
    'CertifierError',
    'CertifierValueError',
    'CertifierTypeError',
]


class CertifierError(Exception):
    def __init__(self, message, value=None, required=None):
        super(CertifierError, self).__init__(message)


class CertifierValueError(CertifierError, ValueError):
    pass


class CertifierTypeError(CertifierError, TypeError):
    pass
