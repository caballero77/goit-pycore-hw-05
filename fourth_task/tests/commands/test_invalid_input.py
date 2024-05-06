"""Tests for invalid_input command."""

import pytest
from commands.invalid_input import invalid_input
from commands.event import EventType

@pytest.mark.parametrize("command", [
    ([], True),
    (["all"], True),
    (["add", "name", "phone"], True),
    (["change", "name", "phone"], True),
])
def test_invalid_input_selector(command):
    """Test invalid_input selector function."""
    assert invalid_input()[0](command) is True

@pytest.mark.parametrize("command", [
    [],
    ["all"],
    ["add", "name", "phone"],
    ["change", "name", "phone"],
])
def test_invalid_input_validator(command):
    """Test invalid_input validator function."""
    assert invalid_input()[1](command) == (True, None)

@pytest.mark.parametrize("command", [
    ["all"],
    ["add", "name", "phone"],
    ["change", "name", "phone"],
])
def test_invalid_input_action(command):
    """Test invalid_input action function."""
    result = invalid_input()[2](command)
    assert result.type == EventType.PRINT
    assert result.payload["print"] == "Invalid command."
