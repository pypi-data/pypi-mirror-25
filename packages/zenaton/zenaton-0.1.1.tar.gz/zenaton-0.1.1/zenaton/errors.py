from __future__ import absolute_import, print_function, unicode_literals


class ZenatonError(Exception):
    pass


class APIError(ZenatonError):
    pass


class UnauthenticatedError(APIError):
    pass
