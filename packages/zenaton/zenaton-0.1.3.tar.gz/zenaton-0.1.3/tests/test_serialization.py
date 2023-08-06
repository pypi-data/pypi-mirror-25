from __future__ import absolute_import, print_function, unicode_literals

import json

import pytest

from zenaton.serialization import Serializable


class MyClass(Serializable):
    pass


class NotSerializable:
    pass


class TestSerializable:

    def test_init_properties(self):
        obj = MyClass(a=1)
        assert obj.a == 1

    def test_invalid_property_name(self):
        from zenaton.serialization import InvalidPropertyError
        with pytest.raises(InvalidPropertyError):
            obj = MyClass(_a=1)

    def test_create(self):
        obj = Serializable.create('test_serialization:MyClass', {'a': 1})
        assert isinstance(obj, MyClass)
        assert obj.a == 1

    def test_create_not_subclass(self):
        from zenaton.serialization import InvalidClassError

        class Thing(Serializable):
            pass

        with pytest.raises(InvalidClassError) as exc_info:
            Thing.create('test_serialization:MyClass', {'a': 1})
        assert str(exc_info.value) == 'Not a Thing'


class TestSerialize:

    def test_serialize_none(self):
        from zenaton.serialization import serialize
        assert serialize(None) == "null"

    def test_serialize_list(self):
        from zenaton.serialization import serialize
        assert json.loads(serialize([1, 2])) == [1, 2]

    def test_serialize_dict(self):
        from zenaton.serialization import serialize
        assert json.loads(serialize({"a": 1, "b": 2})) == {
            "a": 1,
            "b": 2,
        }

    def test_serialize_serializable_object(self):
        from zenaton.serialization import serialize
        obj = MyClass(a=1, b=2)
        assert json.loads(serialize(obj)) == {
            "name": "test_serialization:MyClass",
            "properties": {"a": 1, "b": 2},
        }

    def test_serialize_non_serializable_object(self):
        from zenaton.serialization import serialize, SerializeError

        with pytest.raises(SerializeError):
            serialize(NotSerializable())


class TestDeserialize:

    def test_deserialize_none(self):
        from zenaton.serialization import deserialize
        assert deserialize(None) is None

    def test_deserialize_null(self):
        from zenaton.serialization import deserialize
        assert deserialize('null') is None

    def test_deserialize_list(self):
        from zenaton.serialization import deserialize
        assert deserialize('[1, 2]') == [1, 2]

    def test_deserialize_dict(self):
        from zenaton.serialization import deserialize
        assert deserialize('{"a": 1}') == {"a": 1}

    def test_deserialize_object(self):
        from zenaton.serialization import deserialize
        obj = deserialize(
            '{"name": "test_serialization:MyClass",'
            ' "properties": {"a": 1, "b": 2}}'
        )
        assert isinstance(obj, MyClass)

    def test_deserialize_error(self):
        from zenaton.serialization import deserialize, DeserializeError
        with pytest.raises(DeserializeError):
            deserialize('invalid')
