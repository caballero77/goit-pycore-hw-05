from handler import compose_handlers
from commands.event import EventType, Event
from commands.types import Handler
import pytest

@pytest.mark.parametrize("handlers,command,expected", [
    ([lambda _1,_2: Event(EventType.END, {})], ["first"], Event(EventType.END, {})),
    ([], ["first"], Event(EventType.CONTINUE, {})),
    ([lambda _, next: next, lambda command,
      next: Event(EventType.ERROR, {"message": "Test Error"})],
      ["first"],
      Event(EventType.ERROR, {"message": "Test Error"})),
])
def test_compose_handlers(handlers: list[Handler], command: list[str], expected: Event):
    handler = compose_handlers(handlers)
    result = handler(command)
    assert result.type == expected.type
    assert result.payload == expected.payload
