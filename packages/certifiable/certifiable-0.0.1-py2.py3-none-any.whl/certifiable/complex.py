#!/usr/bin/env python
# -*- coding: latin-1 -*-

from .utils import make_certifier

__all__ = [
    'certify_set',
    'certify_dict',
    'certify_tuple',
    'certify_list',
    'certify_iterable',
    'certify_email',
    'certify_json',
    'certify_html',
]


@make_certifier()
def certify_set(*args, **kwargs):
    pass


@make_certifier()
def certify_dict(*args, **kwargs):
    pass


@make_certifier()
def certify_tuple(*args, **kwargs):
    pass


@make_certifier()
def certify_list(*args, **kwargs):
    pass


@make_certifier()
def certify_iterable(*args, **kwargs):
    pass


@make_certifier()
def certify_email(*args, **kwargs):
    pass


@make_certifier()
def certify_json(*args, **kwargs):
    pass


@make_certifier()
def certify_html(*args, **kwargs):
    pass
