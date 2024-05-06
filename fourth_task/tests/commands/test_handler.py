"""Tests for the handler module."""

import pytest
from commands.handlers import build_handler

@pytest.mark.parametrize("handler,command,expected", [
    (lambda: (lambda x: x == 'exit', lambda _: (True, None), lambda _: 'exit'), 'exit', 'exit'),
    (lambda: (lambda x: x == 'exit', lambda _: (False, "invalid"), lambda _: 'exit'), 'exit', 'invalid'),
    (lambda: (lambda x: x == 'exit', lambda _: (True, None), lambda _: 'exit'), 'net_exit', None),
])
def test_build_handler(handler, command, expected):
    """Test build_handler function."""
    handler = build_handler(handler)
    result = handler(command, None)
    assert result == expected
