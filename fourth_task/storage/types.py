from typing import Callable
from typing import NamedTuple, Tuple

AddOrUpdateContact = Callable[[str, str], None]
GetContact = Callable[[str], Tuple[bool, str]]
GetAllContacts = Callable[[], dict[str, str]]

class Storage(NamedTuple):
    """A named tuple that contains the functions to interact with the storage."""
    add_contact: AddOrUpdateContact
    """The function to add or update a contact in the storage."""
    get_contact: GetContact
    """The function to get a contact from the storage."""
    get_all_contacts: GetAllContacts
    """The function to get all contacts from the storage."""