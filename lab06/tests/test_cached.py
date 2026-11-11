from collections.abc import Callable

from decorators import cached_with_ttl


def test_cached_ttl_and_invalidation(
    fake_clock: tuple[Callable[[], float], Callable[[float], None]],
) -> None:
    clock, advance = fake_clock
    calls = 0

    @cached_with_ttl(ttl=10.0, clock_fn=clock)
    def expensive(x: int) -> int:
        nonlocal calls
        calls += 1
        return x * x

    assert expensive(4) == 16
    assert calls == 1

    assert expensive(4) == 16
    assert calls == 1

    advance(5.0)
    assert expensive(4) == 16
    assert calls == 1

    advance(6.0)  # total 11 > 10.0 TTL expired
    assert expensive(4) == 16
    assert calls == 2

    # Invalidation
    invalidate_fn = expensive.invalidate
    invalidate_fn()
    assert expensive(4) == 16
    assert calls == 3
