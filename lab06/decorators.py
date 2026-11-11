from __future__ import annotations

import functools
import random
import threading
import time
from collections.abc import Callable
from typing import Any, Literal, ParamSpec, Protocol, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")
R_co = TypeVar("R_co", covariant=True)

Key = tuple[tuple[Any, ...], tuple[tuple[str, Any], ...]]


class Decorator(Protocol):
    def __call__(self, func: Callable[P, R], /) -> Callable[P, R]: ...


class CachedFn(Protocol[P, R_co]):
    __name__: str
    __doc__: str | None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...

    def cache_clear(self) -> None: ...

    def cache_invalidate(
        self, predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]
    ) -> int: ...

    def cache_size(self) -> int: ...


class CacheDecorator(Protocol):
    def __call__(self, func: Callable[P, R], /) -> CachedFn[P, R]: ...


class StatsRecord:
    def __init__(self) -> None:
        self.total_calls: int = 0
        self.successes: int = 0
        self.failures: int = 0
        self.total_duration: float = 0.0

    @property
    def avg_duration(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.total_duration / self.total_calls


class StatsFn(Protocol[P, R_co]):
    stats: StatsRecord
    __name__: str
    __doc__: str | None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...


def timed(
    label: str | None = None,
    *,
    unit: Literal["s", "ms", "us"] = "ms",
    logger: Callable[[str], None] = print,
    clock: Callable[[], float] = time.perf_counter,
) -> Decorator:
    factor = {"s": 1.0, "ms": 1e3, "us": 1e6}[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = clock()
            try:
                return func(*args, **kwargs)
            finally:
                logger(f"[timed] {name} took {(clock() - t0) * factor:.3f} {unit}")

        return wrapper

    return decorator


def retries(
    attempts: int = 3,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    delay: float = 0.0,
    backoff: float = 1.0,
    jitter: float = 0.0,
    *,
    sleep: Callable[[float], None] = time.sleep,
    logger: Callable[[str], None] = lambda _: None,
    rand: Callable[[], float] = random.random,
) -> Decorator:
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if i == attempts:
                        logger(f"[retries] fail after {i} attempts: {e!r}")
                        raise
                    wait = delay * backoff ** (i - 1) + (
                        rand() * jitter if jitter else 0.0
                    )
                    logger(f"[retries] attempt {i} failed: {e!r}; sleeping {wait:.3f}s")
                    sleep(wait)
            raise AssertionError("unreachable")

        return wrapper

    return decorator


def make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Key:
    return (args, tuple(sorted(kwargs.items())))


def cached(
    *,
    ttl: float | None = None,
    time_fn: Callable[[], float] = time.time,
) -> CacheDecorator:
    def decorator(func: Callable[P, R]) -> CachedFn[P, R]:
        cache: dict[Key, tuple[float | None, R]] = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(args, kwargs)
            now = time_fn()
            with lock:
                if key in cache:
                    expiry, value = cache[key]
                    if expiry is None or now < expiry:
                        return value
                    del cache[key]
            value = func(*args, **kwargs)
            with lock:
                cache[key] = (None if ttl is None else now + ttl, value)
            return value

        def cache_clear() -> None:
            with lock:
                cache.clear()

        def cache_invalidate(
            predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool],
        ) -> int:
            with lock:
                doomed = [k for k in cache if predicate(k[0], dict(k[1]))]
                for k in doomed:
                    del cache[k]
            return len(doomed)

        def cache_size() -> int:
            with lock:
                return len(cache)

        wrapper_any: Any = wrapper
        wrapper_any.cache_clear = cache_clear
        wrapper_any.cache_invalidate = cache_invalidate
        wrapper_any.cache_size = cache_size
        return cast(CachedFn[P, R], wrapper)

    return decorator


cached_with_ttl = cached


def call_stats(
    clock: Callable[[], float] = time.perf_counter,
) -> Callable[[Callable[P, R]], StatsFn[P, R]]:
    def decorator(func: Callable[P, R]) -> StatsFn[P, R]:
        stats_record = StatsRecord()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            stats_record.total_calls += 1
            t0 = clock()
            try:
                res = func(*args, **kwargs)
                stats_record.successes += 1
                return res
            except Exception:
                stats_record.failures += 1
                raise
            finally:
                stats_record.total_duration += max(0.0, clock() - t0)

        wrapper_any: Any = wrapper
        wrapper_any.stats = stats_record
        return cast(StatsFn[P, R], wrapper)

    return decorator
