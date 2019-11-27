from protomock import registry, errors

import pytest

@pytest.fixture(scope='function')
def test_registry():
    return registry.MockRegistry()

class TestMockRegistry:

    @staticmethod
    def test_add_mock_for_message(test_registry):
        test_registry['simple_message'] = int
        assert test_registry['simple_message']() == 0
        test_registry['simple_message'] = str
        assert test_registry['simple_message']() == 0

    @staticmethod
    def test_get_mock_class(test_registry):
        with pytest.raises(errors.NoMockFoundError):
            test_registry['dne']
