"""This module contains tests for the show_all command."""

import pytest
from commands.show_all import show_all
from commands.event import EventType, Event
from storage.in_memory import init_storage

@pytest.mark.parametrize("command,expected", [
    (["all"], True),
    (["all", "phones"], True),
    (["show"], False),
    ([], False),
])
def test_show_all_selector(command, expected):
    """Test show_all selector function"""
    storage = init_storage()
    assert show_all(storage)()[0](command) == expected

@pytest.mark.parametrize("command,expected", [
    ([], (True, None)),
    (["phones"],
     (False, Event(
         EventType.ERROR,
         {"message": "Invalid arguments: all command does not take any arguments."}
        ))),
])
def test_show_all_validator(command, expected):
    """Test show_all validator function"""
    storage = init_storage()
    assert show_all(storage)()[1](command) == expected

@pytest.mark.parametrize("initial,expected", [
    ({}, ""),
    ({"name": "phone"}, "name: phone"),
    ({"name": "phone", "robert": "roberts_phone"}, "name: phone\nrobert: roberts_phone"),
])
def test_show_all_action(initial, expected):
    """Test show_all action function"""
    storage = init_storage(initial)
    action = show_all(storage)()[2]
    result = action(["all"])
    assert result.type == EventType.PRINT
    assert result.payload["print"] == expected
