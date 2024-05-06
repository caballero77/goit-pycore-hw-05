"""Module that contains a function that calculates the nth Fibonacci number using memoization."""
from typing import Callable

def caching_fibonacci() -> Callable[[int], int]:
    """Return a function that calculates the nth Fibonacci number using memoization."""
    cache = {}
    def fibonacci(n: int) -> int:
        """Memoized function that return the nth Fibonacci number.
        
        Args:
            n (int): The index of the Fibonacci number."""
        if n < 0:
            return 0
        if n in (1, 2):
            return 1
        if n in cache:
            return cache[n]
        result = fibonacci(n - 1) + fibonacci(n - 2)
        cache[n] = result
        return result
    return fibonacci
