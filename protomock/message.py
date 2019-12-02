"""Mocked protobuf messages."""

from typing import Any, Dict

from google.protobuf.message import Message
from google.protobuf.pyext._message import FieldDescriptor, Descriptor as MessageDescriptor

from protomock.field import FieldValueProvider
from protomock.errors import UnknownFieldError

class MockMessage(Message):
    """A read-only mock of a message.

    Args:
        message_descriptor: The descriptor of the message
        field_provider: The field provider from which values should be sourced.
        predefine (optional): Whether or not to predefine all fields. Default is `False`

    Attributes:
        DESCRIPTOR: The `MessageDescriptor` for the message class

    """

    def __init__(self, message_descriptor: MessageDescriptor, field_provider: FieldValueProvider,
                 predefine: bool = False):
        super().__init__()
        self.DESCRIPTOR = message_descriptor  # pylint: disable=invalid-name; Just copying protobuf
        self._values: Dict[str, Any] = {}
        self._provider = field_provider
        self.predefine = predefine

        if self.predefine:
            self.define_all()

    def define_all(self):
        """Define all fields in the Message. This will define all fields in nested Messages."""
        for field_name, field_descriptor in self.DESCRIPTOR.fields_by_name.items():
            self.__getattr__(field_name)
            if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
                self.__getattr__(field_name).define_all()

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
                    field_repr = '\n'.join(f'  {field}' for field in repr(self._values[field_name]).splitlines())
                    if field_repr:
                        entries.append(f'{field_name} {{\n{field_repr}\n}}')
                elif field_desc.type == FieldDescriptor.TYPE_ENUM:
                    value = self._values[field_name]
                    entries.append(f'{field_name}: {value.name}')
                else:
                    value = self._values[field_name]
                    if isinstance(value, str):
                        value = f'"{value}"'
                    elif isinstance(value, bool):
                        value = str(value).lower()
                    entries.append(f'{field_name}: {value}')
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

        Raises:
            UnknownFieldError: If a field is request that is unknown the Message

        """
        try:
            field_descriptor = self.DESCRIPTOR.fields_by_name[name]
        except KeyError:
            raise UnknownFieldError(name, self.DESCRIPTOR.full_name)
        if name not in self._values:
            value = self._provider[field_descriptor]
            self._values[name] = value
        value = self._values[name]
        if field_descriptor.type == FieldDescriptor.TYPE_ENUM:
            value = value.number
        return value
