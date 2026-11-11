from collections.abc import Callable

import pytest
from decorators import StatsRecord, call_stats


def test_call_stats_tracking(
    fake_clock: tuple[Callable[[], float], Callable[[float], None]],
) -> None:
    clock, advance = fake_clock

    @call_stats(clock_fn=clock)
    def compute(x: int, should_fail: bool = False) -> int:
        advance(0.5)
        if should_fail:
            raise ValueError("fail")
        return x * 10

    assert compute(2) == 20
    assert compute(3) == 30

    with pytest.raises(ValueError):
        compute(4, should_fail=True)

    stats: StatsRecord = compute.stats
    assert stats.total_calls == 3
    assert stats.successes == 2
    assert stats.failures == 1
    assert stats.total_duration == 1.5
    assert stats.avg_duration == 0.5
