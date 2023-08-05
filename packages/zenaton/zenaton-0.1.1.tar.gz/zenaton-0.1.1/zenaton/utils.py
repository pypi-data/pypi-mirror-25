from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime
import calendar


def has_method(obj, name):
    return hasattr(obj, name) and callable(getattr(obj, name))


def utc_timestamp():
    return datetime_to_timestamp(datetime.utcnow())


def datetime_to_timestamp(dt):
    return calendar.timegm(dt.utctimetuple())
