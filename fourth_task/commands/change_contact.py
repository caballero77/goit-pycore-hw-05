"""Module with the 'change' command."""

from typing import Tuple
from commands.types import Command
from commands.event import EventType, Event
from commands.errors import MissingArgumentsError, InvalidArgumentsError, input_error
from storage.types import Storage

def change_contact(storage: Storage) -> Command:
    """Returns the 'change' command"""
    def select(command: list[str]) -> bool:
        """Check if the command is 'change'.
        
        Args:
            command (list[str]): The command to check."""
        return len(command) > 0 and command[0] == "change"

    @input_error
    def validate(command: list[str]) -> Tuple[bool, Event]:
        """Valicates the command.
        
        Args:
            command (list[str]): The command to validate."""
        match len(command):
            case 0:
                raise MissingArgumentsError("name and phone number")
            case 1:
                raise MissingArgumentsError("phone number")
            case 2:
                if not storage.get_contact(command[0])[0]:
                    raise InvalidArgumentsError(f"Contact you are trying to update not found: {command[0]}")
                return (True, None)
            case _:
                raise InvalidArgumentsError("change command takes only two arguments.")

    def action(command: list[str]) -> Event:
        """Update the contact with the given name and phone number.

        Args:
            command (list[str]): The command to execute.
            First element is the name of the contact, second element is the new phone number.
        """
        storage.add_contact(command[0], command[1])
        return Event(EventType.PRINT, { "print": f"Contact {command[0]} changed." })

    return lambda: (select, validate, action)
