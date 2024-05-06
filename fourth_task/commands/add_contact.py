"""This module contains the 'add' command. It adds a new contact to the storage."""

from typing import Tuple
from commands.types import Command
from commands.event import Event, EventType
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.types import Storage

def add_contact(storage: Storage) -> Command:
    """Returns the 'add' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'add'
        
        Args:
            command (list[str]): The command to check."""

        return len(command) > 0 and command[0] == "add"

    @input_error
    def valifate(command: list[str]) -> Tuple[bool, Event]:
        """Check if the command has two arguments.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name and phone number")
            case 1:
                raise MissingArgumentsError("phone number")
            case 2:
                return (True, None)
            case _:
                raise InvalidArgumentsError("add command takes only two arguments.")

    def action(command: list[str]) -> Event:
        """Add a new contact with the given name and phone number.
        
        Args:
            command (list[str]): The command to execute. First element is the name of the contact,
            second element is the phone number.
        """
        storage.add_contact(command[0], command[1])
        return Event(EventType.PRINT, {"print": f"Contact {command[0]} added."})
    return lambda: (select, valifate, action)
