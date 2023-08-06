#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

from .utils import make_certifier

__all__ = [
    'certify_printable',
    'certify_text',
    'certify_int',
    'certify_number',
    'certify_bool',
    'certify_bytes',
    'certify_enum',
    'certify_enum_value',
    'certify_object',
    'certify_timestamp',
    'certify_date',
]


@make_certifier()
def certify_printable(*args, **kwargs):
    pass


@make_certifier()
def certify_text(*args, **kwargs):
    pass


@make_certifier()
def certify_string(*args, **kwargs):
    pass


@make_certifier()
def certify_int(*args, **kwargs):
    pass


@make_certifier()
def certify_number(*args, **kwargs):
    pass


@make_certifier()
def certify_bool(*args, **kwargs):
    pass


@make_certifier()
def certify_bytes(*args, **kwargs):
    pass


@make_certifier()
def certify_enum(*args, **kwargs):
    pass


@make_certifier()
def certify_enum_value(*args, **kwargs):
    pass


@make_certifier()
def certify_object(*args, **kwargs):
    pass


@make_certifier()
def certify_timestamp(*args, **kwargs):
    pass


@make_certifier()
def certify_date(*args, **kwargs):
    pass
