from collections.abc import Iterator

from streams import sliding_window, take
from transactions import filter_positive


def test_laziness_evaluated_only_requested() -> None:
    evaluations = 0

    def traced_stream() -> Iterator[float]:
        nonlocal evaluations
        val = 10.0
        while True:
            evaluations += 1
            yield val
            val += 10.0

    stream = traced_stream()
    result = list(take(4, stream))

    assert result == [10.0, 20.0, 30.0, 40.0]
    assert evaluations == 4


def test_filter_laziness() -> None:
    evaluations = 0

    def mixed_stream() -> Iterator[float]:
        nonlocal evaluations
        vals = [10.0, -5.0, 20.0, -15.0, 30.0, -25.0, 40.0, -35.0, 50.0]
        for v in vals:
            evaluations += 1
            yield v

    pos = filter_positive(mixed_stream())
    res = list(take(2, pos))

    assert res == [10.0, 20.0]
    assert evaluations == 3


def test_sliding_window_laziness() -> None:
    evaluations = 0

    def endless() -> Iterator[int]:
        nonlocal evaluations
        x = 1
        while True:
            evaluations += 1
            yield x
            x += 1

    windows = list(take(2, sliding_window(endless(), 3)))
    assert windows == [(1, 2, 3), (2, 3, 4)]
    assert evaluations == 4
