#!/usr/bin/env python
# -*- coding: latin-1 -*-
#

import six

from .errors import CertifierTypeError

_undefined = object()


def make_certifier():
    def decorator(func):
        @six.wraps(func)
        def wrapper(value=_undefined, **kwargs):
            def certify(val):
                func(val, **kwargs)

            if value is not _undefined:
                certify(value)
            else:
                return certify

        return wrapper

    return decorator


def certify_required(value, required=False):
    if value is None:
        if required:
            raise CertifierTypeError(
                message="required value is None",
            )
