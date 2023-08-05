from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import os
from collections import OrderedDict

from zenaton.compat import JSONDecodeError
from zenaton.errors import ZenatonError
from zenaton.instantiation import instantiate_class


log = logging.getLogger(__name__)


class SerializeError(ZenatonError):
    pass


class DeserializeError(ZenatonError):
    pass


class InvalidPropertyError(ZenatonError):
    pass


class InvalidClassError(ZenatonError):
    pass


class Serializable:
    """
    Mixin for (de)serializable classes.
    """

    def __init__(self, **properties):
        """
        Default constructor initializing properties from keyword args
        """
        self.update_properties(properties)

    def update_properties(self, properties):
        for name, value in properties.items():
            if name.startswith('_'):
                msg = "Invalid property name '{}'".format(name)
                raise InvalidPropertyError(msg)
            setattr(self, name, value)

    @classmethod
    def create(cls, class_path, properties):
        obj = instantiate_class(class_path, properties)
        if not isinstance(obj, cls):
            raise InvalidClassError('Not a {}'.format(cls.__name__))
        return obj


def serialize(obj):
    try:
        return json.dumps(obj, default=_default)
    except TypeError:
        msg = 'Cannot serialize {}'.format(obj)
        log.exception(msg)
        raise SerializeError(msg)


def _default(obj):
    if isinstance(obj, Serializable):
        return OrderedDict([
            ('name', get_class_path(obj.__class__)),
            ('properties', get_properties(obj)),
        ])
    raise TypeError


def get_properties(obj):
    return {
        key: value
        for key, value in vars(obj).items()
        if not key.startswith('_')
    }


def get_class_path(class_):
    return '{}:{}'.format(
        get_module_name(class_),
        class_.__name__,
    )


def get_module_name(class_):
    if class_.__module__ == '__main__':
        import __main__
        module_path = os.path.normpath(__main__.__file__)
        root, ext = os.path.splitext(module_path)
        return '.'.join(root.split(os.sep))
    return class_.__module__


def deserialize(text):
    """
    Deserialize an object from the API
    """
    if text is None:
        return None
    try:
        return json.loads(
            text,
            object_hook=_object_hook,
        )
    except JSONDecodeError as exc:
        raise DeserializeError("Invalid JSON: {}".format(exc))


def _object_hook(obj):
    if set(obj.keys()) == {'name', 'properties'}:
        class_path = obj['name']
        return instantiate_class(
            class_path=class_path,
            properties=obj['properties'],
        )
    return obj
