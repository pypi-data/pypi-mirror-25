from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict

import pytest

from zenaton.testing.compat import patch


class DummyClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b


NOT_A_CLASS = {}


def test_instantiate():
    from zenaton.instantiation import instantiate_class

    obj = instantiate_class('test_instantiation:DummyClass', {
        "a": 1,
        "b": 2,
    })

    assert isinstance(obj, DummyClass)
    assert obj.a == 1
    assert obj.b == 2


@patch('zenaton.instantiation.import_module')
def test_instantiate_import_module_error(mock_import):
    from zenaton.instantiation import instantiate_class, ImportModuleError

    mock_import.side_effect = ImportError

    with pytest.raises(ImportModuleError):
        instantiate_class('non_existing_module:Class', {})


def test_instantiate_class_not_found():
    from zenaton.instantiation import instantiate_class, ClassNotFoundError

    with pytest.raises(ClassNotFoundError):
        instantiate_class('test_instantiation:NonExistingClass', {})


def test_instantiate_not_a_class():
    from zenaton.instantiation import instantiate_class, NotAClassError

    with pytest.raises(NotAClassError):
        instantiate_class('test_instantiation:NOT_A_CLASS', {})


def test_instantiate_invalid_property():
    from zenaton.instantiation import instantiate_class, InvalidProperty

    with pytest.raises(InvalidProperty) as exc_info:
        instantiate_class('test_instantiation:DummyClass', {
            "_a": 1,
            "b": 2,
            "c": 3,
        })

    assert str(exc_info.value) == "Property name '_a' is not allowed"


def test_instantiate_invalid_properties():
    from zenaton.instantiation import instantiate_class, InvalidProperty

    with pytest.raises(InvalidProperty) as exc_info:
        instantiate_class('test_instantiation:DummyClass', OrderedDict([
            ("_a", 1),
            ("b", 2),
            ("_c", 3),
        ]))

    assert str(exc_info.value) == "Property names '_a', '_c' are not allowed"


def test_instantiate_constructor_error():
    from zenaton.instantiation import instantiate_class, ConstructorError

    with pytest.raises(ConstructorError) as exc_info:
        instantiate_class('test_instantiation:DummyClass', {
            "a": 1,
            "b": 2,
            "c": 3,
        })
