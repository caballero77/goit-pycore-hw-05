from storage.types import Storage

def __add_contact(memory):
    """Returns a function that adds a contact to the memory."""
    def inner(name, phone):
        memory[name] = phone
    return inner

def __get_contact(memory):
    """Returns a function that gets a contact from the memory."""
    def inner(name):
        if name not in memory:
            return False, None
        return True, memory.get(name)
    return inner

def __get_all_contacts(memory):
    """Returns a function that gets all contacts from the memory."""
    def inner():
        return memory.copy()
    return inner


def init_storage(memory = None) -> Storage:
    """Initializes the in memroy storage with the given initial value of memory.
    
    Args:
        memory (dict[str, str]): The initial value of the memory. Default is {}.
    
    Returns:
        Storage: The in memory storage."""
    if memory is None:
        memory = {}
    return Storage(
        __add_contact(memory),
        __get_contact(memory),
        __get_all_contacts(memory)
    )