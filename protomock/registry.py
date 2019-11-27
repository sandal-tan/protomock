"""A registry for registering mocks for proto-items."""

from google.protobuf.pyext._message import Descriptor as MessageDescriptor

from protomock.errors import NoMockFoundError
from protomock.message import MockMessage

class MockRegistry:
    """A registry for registering mocks for messages."""

    def __init__(self):
        self._registry = {}

    def add_mock_for_message(self, message_descriptor: MessageDescriptor):
        """Add a mock for a message.

        Args:
            message_descriptor: The descriptor of the message for which a mock is registered
            mock_class: The class with which the mock will be generated.

        """
        if message_descriptor in self._registry:
            return

        self._registry[message_descriptor.full_name] = lambda f: MockMessage(message_descriptor, f)

    def get_mock_class(self, message_name) -> 'MockMessage':
        """Get a mock class for a message.

        Args:
            message_name: The name of  the message for which a mock should be retrieved.

        Returns:
            The MockMessage class for ``message_name``

        Raises:
            NoMockFoundError: Raised when a mock cannot be found for a message

        """
        try:
            return self._registry[message_name]
        except KeyError:
            raise NoMockFoundError(message_name)

    def __getitem__(self, item_name):
        return self.get_mock_class(item_name)

    def __setitem__(self, item_name, item):
        self.add_mock_for_message(item_name, item)

    def __contains__(self, item_name):
        return item_name in self._registry
