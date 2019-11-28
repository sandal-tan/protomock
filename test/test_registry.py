from dataclasses import dataclass

import pytest

from protomock import registry, errors
from protos import message_pb2


    

@pytest.fixture(scope='function')
def test_registry():
    r = registry.MockRegistry()
    r.add_mock_for_message(message_pb2.SimpleMessage.DESCRIPTOR)
    return r

class TestMockRegistry:

    @staticmethod
    def test_add_mock_for_message(test_registry):
        message = test_registry['simple_message'] == 0

    @staticmethod
    def test_get_mock_class(test_registry):
        with pytest.raises(errors.NoMockFoundError):
            test_registry['dne']
