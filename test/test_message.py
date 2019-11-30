from dataclasses import dataclass


from protomock import message, errors
from protos import message_pb2

@dataclass(repr=False)
class MockedSimpleClass:

    name: str = 'test'
    count: int = 42
    decimal: float = 42.0
    is_simple: bool = True

    def __repr__(self):
        return f'''name: "{self.name}"
decimal: {self.decimal}
count: {self.count}
is_simple: {str(self.is_simple).lower()}'''

import pytest
class PatchedProvider:

    mocked_simple_class = MockedSimpleClass()

    @classmethod
    def __getitem__(cls, field_descriptor):
        if field_descriptor.full_name == 'DependentMessage.simple_message':
            print(type(field_descriptor.default_value))
        return {
            str: cls.mocked_simple_class.name,
            int: cls.mocked_simple_class.count,
            float: cls.mocked_simple_class.decimal,
            bool: cls.mocked_simple_class.is_simple,
            type(None): cls.mocked_simple_class
        }.get(type(field_descriptor.default_value), cls.mocked_simple_class.name)

@pytest.fixture(scope='function')
def patched_provider():
    return PatchedProvider()

@pytest.fixture(scope='function')
def test_simple_message(patched_provider):
    return message.MockMessage(message_pb2.SimpleMessage.DESCRIPTOR, patched_provider)

@pytest.fixture(scope='function')
def test_dependent_message(patched_provider):
    return message.MockMessage(message_pb2.DependentMessage.DESCRIPTOR, patched_provider)

class TestMessage:

    @staticmethod
    def test_message_get_attr(test_simple_message):
        assert test_simple_message.name == 'test'
        assert test_simple_message.decimal == 42.0
        assert test_simple_message.count == 42
        assert test_simple_message.is_simple

        with pytest.raises(errors.UnknownFieldError):
            test_simple_message.asdf

    @staticmethod
    def test_message_repr(test_dependent_message):
        assert not repr(test_dependent_message)

        test_dependent_message.name
        test_dependent_message.simple_message

        expected = '''name: "test"
simple_message {
  name: "test"
  decimal: 42.0
  count: 42
  is_simple: true
}'''
        assert repr(test_dependent_message) == expected

    @staticmethod
    def test_message_clear(test_simple_message):
        assert isinstance(test_simple_message.count, int)
        assert repr(test_simple_message)
        test_simple_message.Clear()
        assert not repr(test_simple_message)

    @staticmethod
    def test_message_define_all(test_simple_message):
        assert not repr(test_simple_message)
        test_simple_message.define_all()
        expected = '''name: "test"
decimal: 42.0
count: 42
is_simple: true'''
        assert repr(test_simple_message) == expected
