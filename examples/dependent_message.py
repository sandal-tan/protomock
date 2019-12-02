# coding: utf-8
from protomock.field import FieldValueProvider
from protomock.registry import MockRegistry
from protos import message_pb2

registry = MockRegistry()
registry.add_mock_for_message(message_pb2.DependentMessage.DESCRIPTOR)
registry.add_mock_for_message(message_pb2.SimpleMessage.DESCRIPTOR)
registry.add_enum(message_pb2.Color.DESCRIPTOR)
mocked_message = registry['DependentMessage'](predefine=True)
print(mocked_message)
