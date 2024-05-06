from processor import cli_processor
from handler import compose_handlers
from commands.handlers import get_handlers
from commands.types import Dependencies
from storage.in_memory import init_storage

def main():
    storage = init_storage()
    dependencies = Dependencies(storage)

    handlers = get_handlers(dependencies)
    handler = compose_handlers(handlers)

    start = cli_processor(handler)
    start()

if __name__ == "__main__":
    main()