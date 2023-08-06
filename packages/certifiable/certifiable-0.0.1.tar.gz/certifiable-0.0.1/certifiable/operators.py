#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

__all__ = [
    'ANY',
    'AND',
    'ALL',
    'NAND',
    'XOR',
    'certify_only_one',
    'certify_all',
    'certify_none',
    'certify_any',
]


def ANY(*args):
    pass


def AND(*args, **kwargs):
    pass


def NAND(*args, **kwargs):
    pass


def XOR(*args, **kwargs):
    pass


ALL = AND
certify_only_one = XOR
certify_all = AND
certify_none = NAND
certify_any = ANY
