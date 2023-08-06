from __future__ import absolute_import, print_function, unicode_literals

import inspect
import logging
from importlib import import_module

from zenaton.errors import ZenatonError


log = logging.getLogger(__name__)


class InstantiationError(ZenatonError):
    pass


class InvalidClassPath(InstantiationError):
    pass


class ImportModuleError(InstantiationError):
    pass


class ClassNotFoundError(InstantiationError):
    pass


class NotAClassError(InstantiationError):
    pass


class InvalidProperty(InstantiationError):
    pass


class ConstructorError(InstantiationError):
    pass


def instantiate_class(class_path, properties):
    """
    Instantiate an object based on module and class names
    """
    try:
        module_name, class_name = class_path.split(':')
    except ValueError:
        raise InvalidClassPath("Invalid class path '{}'".format(class_path))

    try:
        module = import_module(module_name)
    except ImportError:
        raise ImportModuleError("Could not import module '{}'".format(
            module_name
        ))

    try:
        class_ = getattr(module, class_name)
    except AttributeError:
        raise ClassNotFoundError("Could not find class '{}.{}'".format(
            module_name,
            class_name,
        ))

    if not inspect.isclass(class_):
        raise NotAClassError("'{}' is not a class".format(class_name))

    forbidden_keys = [key for key in properties.keys() if key.startswith('_')]
    if forbidden_keys:
        if len(forbidden_keys) == 1:
            msg = "Property name '{}' is not allowed".format(forbidden_keys[0])
        else:
            msg = "Property names {} are not allowed".format(
                ', '.join(["'{}'".format(key) for key in forbidden_keys])
            )
        raise InvalidProperty(msg)

    try:
        obj = class_(**properties)
    except Exception:
        msg = "Could not create object of class '{}'".format(class_name)
        log.exception(msg)
        raise ConstructorError(msg)

    return obj
