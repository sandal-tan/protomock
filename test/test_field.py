from dataclasses import dataclass

import pytest

from protomock import field, errors
from protos.message_pb2 import SimpleMessage, DependentMessage, Color

class MockedDummy:

    def get_random_value(self):
        return 'color'

@pytest.fixture
def test_provider():
    return field.FieldValueProvider({
        SimpleMessage.DESCRIPTOR.full_name: (lambda _: 'simple_message'),
        Color.DESCRIPTOR.full_name: MockedDummy()
    })


class TestFieldValueProvider:
    
    @staticmethod
    def test_get_value_for_field(test_provider):

        # Test with SimpleMessage fields
        name_value = test_provider[DependentMessage.DESCRIPTOR.fields[0]]
        assert isinstance(name_value, str)

        simple_message_value = test_provider[DependentMessage.DESCRIPTOR.fields[1]]
        assert simple_message_value == 'simple_message'

        name_value = test_provider[SimpleMessage.DESCRIPTOR.fields[0]]
        assert isinstance(name_value, str)

        decimal_value = test_provider[SimpleMessage.DESCRIPTOR.fields[1]]
        assert isinstance(decimal_value, float)

        count_value = test_provider[SimpleMessage.DESCRIPTOR.fields[2]]
        assert isinstance(count_value, int)

        is_simple_value = test_provider[SimpleMessage.DESCRIPTOR.fields[3]]
        assert isinstance(is_simple_value, bool)

        color_value = test_provider[SimpleMessage.DESCRIPTOR.fields[4]]
        assert color_value == 'color'

    @staticmethod
    def test_get_value_for_field_no_provider(test_provider):

        @dataclass
        class MockFieldDescriptor:
            type: int = -1
            full_name: str = 'MockFieldDescriptor'

        with pytest.raises(errors.NoProviderError):
            test_provider[MockFieldDescriptor()]
