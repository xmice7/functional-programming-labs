from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def take(n: int, it: Iterable[T]) -> Iterator[T]:
    if n < 0:
        raise ValueError("n must be non-negative")
    return islice(it, n)


def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    if n < 0:
        raise ValueError("n must be non-negative")
    iterator = iter(it)
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            return
    yield from iterator


def sliding_window(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    if k <= 0:
        raise ValueError("k must be greater than 0")
    iterator = iter(it)
    window: deque[T] = deque(islice(iterator, k), maxlen=k)
    if len(window) < k:
        return
    yield tuple(window)
    for elem in iterator:
        window.append(elem)
        yield tuple(window)


def fib_stream() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
