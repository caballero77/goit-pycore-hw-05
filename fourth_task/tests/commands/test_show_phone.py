"""Tests for show_phone command."""

import pytest
from commands.show_phone import show_phone
from commands.event import EventType, Event
from storage.in_memory import init_storage

@pytest.mark.parametrize("command,expected", [
    (["phone", "name"], True),
    (["phone", "NAME"], True),
    (["phone"], True),
    (["all"], False),
    ([], False),
])
def test_show_phone_selector(command, expected):
    """Test show_phone selector function"""
    storage = init_storage()
    assert show_phone(storage)()[0](command) == expected

@pytest.mark.parametrize("initial,command,expected", [
    ({"name": "test"}, ["name"], (True, None)),
    ({"NAME": "test"}, ["NAME"], (True, None)),
    ({}, [], (False, Event(EventType.ERROR, {"message": "Missing arguments: name"}))),
    ({}, ["name"], (False, Event(
        EventType.ERROR,
        {"message": "Invalid arguments: Contact you are trying to get not found: name"}
    ))),
    ({"name": "test"}, ["name", "test"], (False, Event(
        EventType.ERROR,
        {"message": "Invalid arguments: phone command takes only one argument."}
    ))),
])
def test_show_phone_validator(initial, command, expected):
    """Test show_phone validator function"""
    storage = init_storage(initial)
    assert show_phone(storage)()[1](command) == expected

@pytest.mark.parametrize("initial,command,expected", [
    ({"name": "phone"}, ["phone", "name"], "phone"),
    ({"NAME": "phone"}, ["phone", "NAME"], "phone"),
    ({"robert": "roberts_phone", "david": "davids_phone"}, ["phone", "robert"], "roberts_phone"),
    ({"robert": "roberts_phone", "david": "davids_phone"}, ["phone", "david"], "davids_phone"),
])
def test_show_phone_action_success(initial, command, expected):
    storage = init_storage(initial)
    action = show_phone(storage)()[2]
    result = action(command[1:])
    assert result.type == EventType.PRINT
    assert result.payload["print"] == expected
