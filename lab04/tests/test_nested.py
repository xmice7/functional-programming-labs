from typing import Any

import pytest
from nested import (
    iterative_max_depth,
    iterative_nested_stats,
    max_depth,
    nested_count,
    nested_stats,
    nested_sum,
)


def test_nested_sum_basic(nested_sample: list[Any]) -> None:
    assert nested_sum(nested_sample) == 55.0


def test_nested_count_basic(nested_sample: list[Any]) -> None:
    assert nested_count(nested_sample) == 10


def test_nested_stats(nested_sample: list[Any]) -> None:
    s, c = nested_stats(nested_sample)
    assert s == 55.0
    assert c == 10


def test_iterative_equivalence(nested_sample: list[Any]) -> None:
    rec_s, rec_c = nested_stats(nested_sample)
    it_s, it_c = iterative_nested_stats(nested_sample)
    assert rec_s == it_s
    assert rec_c == it_c


def test_max_depth(nested_sample: list[Any]) -> None:
    assert max_depth(nested_sample) == 4
    assert iterative_max_depth(nested_sample) == 4


def test_edge_cases() -> None:
    assert nested_sum([]) == 0.0
    assert nested_count([]) == 0
    assert max_depth([]) == 1
    assert nested_sum(42) == 42.0
    assert nested_count(42) == 1
    assert max_depth(42) == 0
    assert nested_sum([True, False, 10]) == 10.0


def test_deeply_nested_structure() -> None:
    depth = 1200
    curr: Any = 1
    for _ in range(depth):
        curr = [curr]

    it_s, it_c = iterative_nested_stats(curr)
    assert it_s == 1.0
    assert it_c == 1
    assert iterative_max_depth(curr) == depth

    with pytest.raises(RecursionError):
        nested_sum(curr)
