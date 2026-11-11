from collections.abc import Callable

from decorators import timed


def test_timed_decorator(
    fake_clock: tuple[Callable[[], float], Callable[[float], None]],
) -> None:
    clock, advance = fake_clock
    records: list[tuple[str, float]] = []

    def sink(name: str, duration: float) -> None:
        records.append((name, duration))

    @timed(sink=sink, clock_fn=clock)
    def task() -> str:
        advance(0.25)
        return "done"

    res = task()
    assert res == "done"
    assert len(records) == 1
    assert records[0] == ("task", 0.25)
