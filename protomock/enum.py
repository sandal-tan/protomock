"""Abstraction for interacting with Protobuf enums."""

import random

from google.protobuf.pyext._message import EnumDescriptor, EnumValueDescriptor

class Enum:
    """Abstraction for dealing with Protobuf enums.

    Args:
        enum_descriptor: The descriptor of the enum

    """

    def __init__(self, enum_descriptor: EnumDescriptor):
        self.descriptor = enum_descriptor

    def get_random_value(self, include_unknown: bool = False) -> EnumValueDescriptor:
        """Get a random value for the Enum, excluding the `UNKNOWN` default value by default.

        Args:
            include_unknown (optional): Whether or not to consider the default `UNKNOWN` value. Default is `False`

        Returns:
            The value descriptor for the enum value

        """
        start = 2 if not include_unknown else 1
        idx = random.randint(start, len(self.descriptor.values)) - 1
        return self.descriptor.values[idx]
