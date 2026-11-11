from collections.abc import Callable

import pytest


@pytest.fixture
def fake_clock() -> tuple[Callable[[], float], Callable[[float], None]]:
    current = 1000.0

    def clock() -> float:
        return current

    def advance(delta: float) -> None:
        nonlocal current
        current += delta

    return clock, advance


@pytest.fixture
def sleep_recorder() -> tuple[Callable[[float], None], Callable[[], list[float]]]:
    delays: list[float] = []

    def sleep(d: float) -> None:
        delays.append(d)

    def get_delays() -> list[float]:
        return list(delays)

    return sleep, get_delays
