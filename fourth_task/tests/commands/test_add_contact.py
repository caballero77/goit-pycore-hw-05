"""Tests for add_contact command"""

import pytest
from commands.add_contact import add_contact
from commands.event import EventType, Event
from storage.in_memory import init_storage

@pytest.mark.parametrize("command,expected", [
    (["add", "name", "phone"], True),
    (["add", "NAME", "PHONE"], True),
    (["add"], True),
    (["add", "name"], True),
    (["change", "name"], False),
    ([], False),
])
def test_add_contact_selector(command: list[str], expected):
    """Test add_contact selector function"""
    storage = init_storage()

    assert add_contact(storage)()[0](command) == expected

@pytest.mark.parametrize("command,expected", [
    (["name", "phone"], (True, None)),
    (["NAME", "PHONE"], (True, None)),
    ([], (False, Event(EventType.ERROR, {"message": "Missing arguments: name and phone number"}))),
    (["name"], (False, Event(EventType.ERROR, {"message": "Missing arguments: phone number"}))),
    (["name", "phone", "extra"], (False, Event(
        EventType.ERROR,
        {"message": "Invalid arguments: add command takes only two arguments."}
    ))),
])
def test_add_contact_validator(command: list[str], expected):
    """Test add_contact validator function"""
    storage = init_storage()

    assert add_contact(storage)()[1](command) == expected

@pytest.mark.parametrize("commands,expected", [
    ([["add", "name", "phone"]], {"name": "phone"}),
    ([["add", "NAME", "PHONE"]], {"NAME": "PHONE"}),
    ([["add", "robert", "roberts_phone"], ["add", "david", "davids_phone"]],
     {"robert": "roberts_phone", "david": "davids_phone"}),
    ([["add", "robert", "roberts_phone"], ["add", "robert", "roberts_new_phone"]],
     {"robert": "roberts_new_phone"}),
])
def test_add_contact_action(commands, expected):
    """Test add_contact action function"""
    storage = init_storage()
    for command in commands:
        result = add_contact(storage)()[2](command[1:])
        assert result.type == EventType.PRINT
    assert storage.get_all_contacts() == expected
