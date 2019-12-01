from protomock import enum

from protos import message_pb2

class TestEnum:

    @staticmethod
    def test_get_random_value():
        e = enum.Enum(message_pb2.Color.DESCRIPTOR)
        
        # Get all non-default values
        for value in message_pb2.Color.DESCRIPTOR.values[1:]:
            random_value = e.get_random_value()
            while random_value.number != value.number:
                random_value = e.get_random_value()
                if random_value.number == 0:
                    assert False, 'An unknown value should not be returned by default.'

        random_value = e.get_random_value(include_unknown=True)
        for _ in range(100):
            if random_value.number == 0:
                break
            random_value = e.get_random_value(include_unknown=True)
        else:
            assert False, 'Unknown value was never returned'
