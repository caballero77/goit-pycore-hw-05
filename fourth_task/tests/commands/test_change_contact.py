"""Tests for change_contact command"""

import pytest
from commands.change_contact import change_contact
from commands.event import EventType, Event
from storage.in_memory import init_storage

@pytest.mark.parametrize("command,expected", [
    (["change", "name", "phone"], True),
    (["change", "NAME", "PHONE"], True),
    (["change"], True),
    (["change", "name"], True),
    (["add", "name"], False),
    (["add"], False),
    ([], False),
])
def test_change_contact_selector(command: list[str], expected):
    """Test change_contact selector function"""
    storage = init_storage()

    assert change_contact(storage)()[0](command) == expected

@pytest.mark.parametrize("initial,command,expected", [
    ({}, ["name", "phone"],
     (False, Event(
         EventType.ERROR,
         {"message": "Invalid arguments: Contact you are trying to update not found: name"}
        ))),
    ({"name": "phone"}, ["not_name", "phone"],
     (False, Event(
         EventType.ERROR,
         {"message": "Invalid arguments: Contact you are trying to update not found: not_name"}
        ))),
    ({"name": "phone"}, ["NAME", "phone"],
     (False, Event(
         EventType.ERROR,
         {"message": "Invalid arguments: Contact you are trying to update not found: NAME"}
        ))),
    ({"name": "phone"}, ["name", "phone"], (True, None)),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     ["robert", "roberts_new_phone"],
     (True, None)),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     ["robert", "roberts_new_phone"],
     (True, None)),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     ["robert", "roberts_new_phone"],
     (True, None)),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     ["robert", "roberts_new_phone", "extra"],
        (False, Event(
            EventType.ERROR,
            {"message": "Invalid arguments: change command takes only two arguments."}
        ))),
])
def test_change_contact_validator(initial, command, expected):
    """Test change_contact validator function"""
    storage = init_storage(initial)

    assert change_contact(storage)()[1](command) == expected

@pytest.mark.parametrize("initial,commands,expected", [
    ({"name": "phone"}, [["change", "name", "new_phone"]], {"name": "new_phone"}),
    ({"name": "phone"}, [["change", "name", "phone"]], {"name": "phone"}),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     [["change", "robert", "roberts_new_phone"]],
     {"robert": "roberts_new_phone", "david": "davids_phone"}),
    ({"robert": "roberts_phone", "david": "davids_phone"},
     [["change", "robert", "roberts_new_phone"], ["change", "david", "davids_new_phone"]],
     {"robert": "roberts_new_phone", "david": "davids_new_phone"}),
])
def test_change_contact_action_success(initial, commands, expected):
    """Test change_contact action function"""
    storage = init_storage(initial)
    action = change_contact(storage)()[2]
    for command in commands:
        result = action(command[1:])
        assert result.type == EventType.PRINT

    assert storage.get_all_contacts() == expected
