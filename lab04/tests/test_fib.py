import pytest
from algorithms import fib_memoized, fib_naive


def test_fib_correctness() -> None:
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for i, exp in enumerate(expected):
        assert fib_naive(i) == exp
        assert fib_memoized(i) == exp


def test_fib_memoization_cache_info() -> None:
    fib_memoized.cache_clear()
    _ = fib_memoized(10)
    info = fib_memoized.cache_info()
    assert info.hits > 0
    assert info.currsize > 0


def test_fib_negative() -> None:
    with pytest.raises(ValueError):
        fib_naive(-1)
    with pytest.raises(ValueError):
        fib_memoized(-1)
