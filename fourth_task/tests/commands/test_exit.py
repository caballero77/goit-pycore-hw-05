"""Tests for the exit command."""

import pytest
from commands.exit import exit
from commands.event import EventType, Event

@pytest.mark.parametrize("command,expected", [
    (["exit"], True),
    (["close"], True),
    (["any", "other", "commands"], False),
])
def test_exit_selector(command, expected):
    """Test exit selector function"""
    assert exit()[0](command) == expected

@pytest.mark.parametrize("command,expected", [
    ([], (True, None)),
    (["any"],
     (False, Event(
         EventType.ERROR,
         {"message": "Invalid arguments: exit command does not take any arguments."}
        )))
])
def test_exit_validator(command, expected):
    """Test exit validator function"""
    assert exit()[1](command) == expected

def test_exit_action():
    """Test exit action function"""
    result = exit()[2](None)
    assert result.type == EventType.END
    assert result.payload["print"] == "Goodbye!"
