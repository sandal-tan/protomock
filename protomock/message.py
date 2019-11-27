"""Mocked protobuf messages."""

from typing import Any

from google.protobuf.message import Message
from google.protobuf.pyext._message import FieldDescriptor, Descriptor as MessageDescriptor

from protomock.field import FieldValueProvider
from protomock.errors import UnknownFieldError

class MockMessage(Message):
    """A read-only mock of a message.

    Args:
        message_descriptor: The descriptor of the message
        field_provider: The field provider from which values should be sourced.

    Attributes:
        DESCRIPTOR: The `MessageDescriptor` for the message class

    """

    def __init__(self, message_descriptor: MessageDescriptor, field_provider: FieldValueProvider):
        super().__init__()
        self.DESCRIPTOR = message_descriptor
        self._values = {}
        self._provider = field_provider

    def Clear(self):
        """Clear all values set in the proto."""
        self._values = {}

    def __str__(self) -> str:
        """Return a string representation of the Message.

        Returns:
            A string representation

        """
        entries = []
        for field_name, field_desc in self.DESCRIPTOR.fields_by_name.items():
            if field_name in self._values:
                if field_desc.type == FieldDescriptor.TYPE_MESSAGE:
                    entries.append(f'{field_name} {{\n{repr(self._values[field_name])}\n}}')
                else:
                    entries.append(f'{field_name}: {repr(self._values[field_name])}')
        return '\n'.join(entries)

    def __repr__(self) -> str:
        """Return a string representation of the Message.

        Returns:
            A string representation

        """
        return str(self)
    
    def __getattr__(self, name: str) -> Any:
        """Get an attribute, by name. This is used to generate and return field values for the message.

        Args:
            name: The name of the field to retrieve

        Returns:
            The value of the field at ``name``

        """
        if name not in self._values:
            try:
                field_descriptor = self.DESCRIPTOR.fields_by_name[name]
            except KeyError:
                raise UnknownFieldError(name, self.DESCRIPTOR.full_name)
            value = self._provider[field_descriptor]
            self._values[name] = value
        return self._values[name]
