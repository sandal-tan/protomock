"""Mocking around message fields."""

from typing import Any, Optional

import faker
from google.protobuf.pyext._message import FieldDescriptor

from protomock.errors import NoProviderError

class FieldValueProvider:
    """A provider for fields.

    Args:
        mock_registry: The mock registry from which messages should be created
        seed (optional): The seed to pass to faker

    """

    def __init__(self, mock_registry, seed: Optional[int] = None):
        self._registry = mock_registry
        self._faker = faker.Faker()
        if seed is not None:
            self._faker.seed(seed)

    def get_value_for_field(self, field: FieldDescriptor) -> Any:
        """Get a value for a field.

        Args:
            field: The field descriptor for which a value returned.

        Returns:
            A value that is valid for ``field``.

        Raises:
            NoProviderError: If a provider cannot be found for a type.

        """
        # pylint: disable=no-member
        if field.type == FieldDescriptor.TYPE_BOOL:
            return self._faker.pybool()

        if field.type == FieldDescriptor.TYPE_BYTES:
            return self._faker.binary()

        if field.type in [FieldDescriptor.TYPE_FLOAT, FieldDescriptor.TYPE_DOUBLE]:
            return self._faker.pyfloat()

        if field.type in [FieldDescriptor.TYPE_INT32, FieldDescriptor.TYPE_INT64]:
            return self._faker.pyint()

        if field.type == FieldDescriptor.TYPE_STRING:
            return self._faker.pystr()

        if field.type == FieldDescriptor.TYPE_ENUM:
            enum_type = field.enum_type.full_name
            return self._registry[enum_type].get_random_value()

        if field.type == FieldDescriptor.TYPE_MESSAGE:
            message_type = field.message_type.full_name
            return self._registry[message_type](self)

        raise NoProviderError(f'Field: {field.full_name}')

    def __getitem__(self, item_name):
        return self.get_value_for_field(item_name)
