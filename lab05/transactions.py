from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from itertools import accumulate, cycle
from typing import TypeVar

from streams import sliding_window

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Transaction:
    tx_id: int
    amount: float
    category: str


def infinite_transaction_stream(
    pattern: tuple[float, ...] = (100.0, -40.0, 250.0, -15.0, 50.0, -120.0, 300.0)
) -> Iterator[float]:
    yield from cycle(pattern)


def filter_positive(amounts: Iterable[float]) -> Iterator[float]:
    return (round(a, 2) for a in amounts if a > 0.0)


def cumulative_balance(
    amounts: Iterable[float], initial_balance: float = 0.0
) -> Iterator[float]:
    return (
        round(val, 2)
        for val in accumulate(
            amounts,
            lambda acc, x: acc + x,
            initial=initial_balance,
        )
    )


def moving_sums(amounts: Iterable[float], k: int) -> Iterator[float]:
    return (round(sum(w), 2) for w in sliding_window(amounts, k))


def moving_averages(amounts: Iterable[float], k: int) -> Iterator[float]:
    return (round(sum(w) / k, 2) for w in sliding_window(amounts, k))
