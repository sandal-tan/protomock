# Protomock

A library to mock Protobuf messages and services.

Protomock works by utilizing the `DESCRIPTOR` object that hangs off of Messages and Fields. Utilizing this as a schema,
values are randomly generated for fields either on request, or all at once. These mocked messages subclass
`google.protobuf.message.Message` and *should* be able to work with gRPC services, I just haven't tested it yet.

# Development

To install development environment:

    $ pipenv install --dev

# Examples:

Print out a predefined, nested Message:

    from protomock.registry import MockRegistry
    from protos import message_pb2
    registry = MockRegistry()
    # The definition of this message depends on `SimpleMessage` but we don't have to add that mock first
    registry.add_mock_for_message(message_pb2.DependentMessage.DESCRIPTOR)
    registry.add_mock_for_message(message_pb2.SimpleMessage.DESCRIPTOR)
    mocked_message = registry['DependentMessage'](predefine=True)
    print(mocked_message)

Example output:

    name: "MEqrdAwwEAaqczasGUnt"
    simple_message {
      name: "MktveEpRimGsHDYmpzWy"
      decimal: -228933.0
      count: 1837
      is_simple: false
    }
