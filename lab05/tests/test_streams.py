import pytest
from streams import drop, fib_stream, sliding_window, take


def test_take_basic() -> None:
    data = [10, 20, 30, 40, 50]
    assert list(take(3, data)) == [10, 20, 30]
    assert list(take(0, data)) == []
    assert list(take(10, data)) == [10, 20, 30, 40, 50]


def test_take_negative() -> None:
    with pytest.raises(ValueError):
        list(take(-1, [1, 2, 3]))


def test_drop_basic() -> None:
    data = [10, 20, 30, 40, 50]
    assert list(drop(2, data)) == [30, 40, 50]
    assert list(drop(0, data)) == [10, 20, 30, 40, 50]
    assert list(drop(10, data)) == []


def test_drop_negative() -> None:
    with pytest.raises(ValueError):
        list(drop(-1, [1, 2, 3]))


def test_sliding_window_basic() -> None:
    data = [1, 2, 3, 4, 5]
    windows = list(sliding_window(data, 3))
    assert windows == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]


def test_sliding_window_edge_cases() -> None:
    assert list(sliding_window([], 3)) == []
    assert list(sliding_window([1, 2], 3)) == []
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], -2))


def test_fib_stream() -> None:
    assert list(take(8, fib_stream())) == [0, 1, 1, 2, 3, 5, 8, 13]
