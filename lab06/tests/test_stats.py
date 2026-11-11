from __future__ import annotations

import pytest
from decorators import call_stats


def test_call_stats_tracking() -> None:
    ticks = iter([0.0, 0.05, 0.1, 0.25, 0.3, 0.4])

    @call_stats(clock=lambda: next(ticks))
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    assert divide(10, 2) == 5.0
    assert divide.stats.total_calls == 1
    assert divide.stats.successes == 1
    assert divide.stats.failures == 0

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    assert divide.stats.total_calls == 2
    assert divide.stats.successes == 1
    assert divide.stats.failures == 1
    assert divide.stats.total_duration > 0.0
    assert divide.stats.avg_duration > 0.0


def test_call_stats_metadata() -> None:
    def original_fn() -> str:
        return "ok"

    decorated = call_stats()(original_fn)
    assert decorated.__name__ == "original_fn"
