from dataclasses import dataclass
import random

import pytest

from protomock import registry, errors
from protos import message_pb2

class PatchedMockMessage:

    def __init__(self, messaage_descriptor, provider, predefine):
       self.init_args = (messaage_descriptor, provider, predefine)

class PatchedProvider:
    @staticmethod
    def __getitem__(item_name):
        return lambda x: x

@pytest.fixture(scope='class')
def patch_mock_message():
    registry.MockMessage = PatchedMockMessage

@pytest.fixture(scope='function')
def provider_value():
    return random.randint(0, 1000)


@pytest.fixture(scope='function')
def patch_provider(provider_value):
    registry.FieldValueProvider = lambda _: provider_value


@pytest.fixture(scope='function')
def test_registry(patch_mock_message, patch_provider):
    r = registry.MockRegistry()
    r.add_mock_for_message(message_pb2.SimpleMessage.DESCRIPTOR)
    return r

class TestMockRegistry:

    @staticmethod
    def test_add_mock_for_message(test_registry, provider_value):
        message = test_registry['SimpleMessage']()
        assert message.init_args == (message_pb2.SimpleMessage.DESCRIPTOR, provider_value, False)

    @staticmethod
    def test_get_mock_class(test_registry):
        with pytest.raises(errors.NoMockFoundError):
            test_registry['dne']
