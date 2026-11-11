from collections.abc import Callable

import pytest
from closures import make_file_simulator, make_logger
from decorators import retries


def test_retries_immediate_success() -> None:
    calls = 0

    @retries(max_attempts=3)
    def ok_fn(x: int) -> int:
        nonlocal calls
        calls += 1
        return x * 2

    assert ok_fn(5) == 10
    assert calls == 1


def test_retries_with_simulated_file(
    sleep_recorder: tuple[Callable[[float], None], Callable[[], list[float]]],
) -> None:
    fake_sleep, get_sleeps = sleep_recorder
    log_fn, get_logs, _ = make_logger()

    sim_read, get_attempts = make_file_simulator(fail_attempts=2, content="data")

    @retries(
        max_attempts=3,
        delay=0.1,
        backoff=2.0,
        exceptions=(OSError,),
        sleep_fn=fake_sleep,
        logger=log_fn,
    )
    def fetch() -> str:
        return sim_read("a.txt")

    assert fetch() == "data"
    assert get_attempts() == 3
    assert get_sleeps() == [0.1, 0.2]
    assert len(get_logs()) == 2


def test_retries_exhausted() -> None:
    sim_read, get_attempts = make_file_simulator(fail_attempts=5, content="data")

    @retries(max_attempts=2, exceptions=(OSError,))
    def fetch() -> str:
        return sim_read("a.txt")

    with pytest.raises(OSError):
        fetch()
    assert get_attempts() == 2


def test_preserves_metadata() -> None:
    def original_fn(x: int) -> int:
        return x + 1

    wrapped = retries(max_attempts=3)(original_fn)
    assert wrapped.__name__ == "original_fn"
    assert wrapped.__wrapped__ is original_fn
