# coding: utf-8
from protomock.field import FieldValueProvider
from protomock.registry import MockRegistry
from protos import message_pb2

if __name__ == '__main__':
    registry = MockRegistry()
    registry.add_mock_for_message(message_pb2.DependentMessage.DESCRIPTOR)
    registry.add_mock_for_message(message_pb2.SimpleMessage.DESCRIPTOR)
    mocked_message = registry['DependentMessage'](predefine=True)
    print(mocked_message)
