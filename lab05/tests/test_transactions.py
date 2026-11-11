from streams import take
from transactions import (
    cumulative_balance,
    filter_positive,
    infinite_transaction_stream,
    moving_averages,
    moving_sums,
)


def test_filter_positive(sample_amounts: list[float]) -> None:
    res = list(filter_positive(sample_amounts))
    assert res == [100.0, 200.0, 300.0, 150.0]


def test_cumulative_balance(sample_amounts: list[float]) -> None:
    res = list(cumulative_balance(sample_amounts, initial_balance=0.0))
    # [0.0, 100.0, 50.0, 250.0, 225.0, 525.0, 445.0, 595.0]
    assert res[0] == 0.0
    assert res[1] == 100.0
    assert res[2] == 50.0
    assert res[-1] == 595.0


def test_moving_sums_and_averages(sample_amounts: list[float]) -> None:
    positive = list(filter_positive(sample_amounts))
    # positive: [100.0, 200.0, 300.0, 150.0]
    sums = list(moving_sums(positive, 2))
    assert sums == [300.0, 500.0, 450.0]

    avgs = list(moving_averages(positive, 2))
    assert avgs == [150.0, 250.0, 225.0]


def test_infinite_stream() -> None:
    stream = infinite_transaction_stream((10.0, -5.0))
    sample = list(take(5, stream))
    assert sample == [10.0, -5.0, 10.0, -5.0, 10.0]
