from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, Protocol, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")
R_co = TypeVar("R_co", covariant=True)


class WrappedFn(Protocol[P, R_co]):
    __name__: str
    __doc__: str | None
    __wrapped__: Callable[..., Any]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...


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
    __wrapped__: Callable[..., Any]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...


class CachedFn(Protocol[P, R_co]):
    __name__: str
    __doc__: str | None
    __wrapped__: Callable[..., Any]

    def invalidate(self) -> None: ...

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...


def retries(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    sleep_fn: Callable[[float], None] | None = None,
    logger: Callable[[str], None] | None = None,
) -> Callable[[Callable[P, R]], WrappedFn[P, R]]:
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(fn: Callable[P, R]) -> WrappedFn[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as err:
                    if logger:
                        logger(f"Attempt {attempt}/{max_attempts} failed: {err}")
                    if attempt == max_attempts:
                        raise
                    if sleep_fn:
                        sleep_fn(current_delay)
                    current_delay *= backoff
            raise RuntimeError("Unreachable")

        return cast(WrappedFn[P, R], wrapper)

    return decorator


def call_stats(
    clock_fn: Callable[[], float] | None = None,
) -> Callable[[Callable[P, R]], StatsFn[P, R]]:
    get_time = clock_fn if clock_fn is not None else (lambda: 0.0)

    def decorator(fn: Callable[P, R]) -> StatsFn[P, R]:
        stats_obj = StatsRecord()

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            stats_obj.total_calls += 1
            t_start = get_time()
            try:
                result = fn(*args, **kwargs)
                stats_obj.successes += 1
                return result
            except BaseException:
                stats_obj.failures += 1
                raise
            finally:
                t_end = get_time()
                stats_obj.total_duration += max(0.0, t_end - t_start)

        cast(Any, wrapper).stats = stats_obj
        return cast(StatsFn[P, R], wrapper)

    return decorator


def timed(
    sink: Callable[[str, float], None] | None = None,
    clock_fn: Callable[[], float] | None = None,
) -> Callable[[Callable[P, R]], WrappedFn[P, R]]:
    get_time = clock_fn if clock_fn is not None else (lambda: 0.0)

    def decorator(fn: Callable[P, R]) -> WrappedFn[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = get_time()
            try:
                return fn(*args, **kwargs)
            finally:
                elapsed = max(0.0, get_time() - t0)
                if sink:
                    sink(fn.__name__, elapsed)

        return cast(WrappedFn[P, R], wrapper)

    return decorator


def cached_with_ttl(
    ttl: float = 60.0,
    clock_fn: Callable[[], float] | None = None,
) -> Callable[[Callable[P, R]], CachedFn[P, R]]:
    get_time = clock_fn if clock_fn is not None else (lambda: 0.0)

    def decorator(fn: Callable[P, R]) -> CachedFn[P, R]:
        cache: dict[tuple[Any, ...], tuple[R, float]] = {}

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            now = get_time()
            if key in cache:
                val, ts = cache[key]
                if now - ts <= ttl:
                    return val

            val = fn(*args, **kwargs)
            cache[key] = (val, now)
            return val

        def invalidate() -> None:
            cache.clear()

        cast(Any, wrapper).invalidate = invalidate
        return cast(CachedFn[P, R], wrapper)

    return decorator
