"""Module that contains functions for the second task."""

import re
from typing import Generator, Callable

def generator_numbers(text: str) -> Generator[float, None, None]:
    """Generator that finds all numbers in the text and yields them."""
    for catch in re.finditer(r"(?<=\s)(-?[\d]+[.][\d]+|-?[\d]+)(?=\s)", f" {text} "):
        yield float(catch[0])

def sum_profit(test: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """Function that calculates the sum of all numbers in the text."""
    return sum(func(test))
