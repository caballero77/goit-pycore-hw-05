"""Tests for hello command."""
import pytest
from commands.hello import hello
from commands.event import EventType, Event

@pytest.mark.parametrize("command,expected", [
    (["hello"], True),
    (["close"], False),
    (["any", "other", "command"], False),
])
def test_hello_selector(command, expected):
    """Test hello selector function"""
    assert hello()[0](command) == expected

@pytest.mark.parametrize("command,expected", [
    ([], (True, None)),
    (["any"], (False, Event(
        EventType.ERROR,
        {"message": "Invalid arguments: hello command does not take any arguments."}
    ))),
])
def test_hello_validator(command, expected):
    """Test hello validator function"""
    assert hello()[1](command) == expected

def test_exit_action():
    """Test hello action function"""
    result = hello()[2](None)
    assert result.type == EventType.PRINT
    assert result.payload["print"] == "How can I help you?"
