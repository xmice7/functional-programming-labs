from __future__ import annotations

from collections.abc import Callable, Iterable


def make_counter(start: int = 0) -> Callable[[], int]:
    value = start

    def inc() -> int:
        nonlocal value
        value += 1
        return value

    return inc


def make_logger(
    prefix: str = "INFO",
    sink: Callable[[str], None] | None = None,
) -> Callable[[str], None]:
    target_sink = sink if sink is not None else print
    return lambda msg: target_sink(f"[{prefix}] {msg}")


def make_file_simulator(
    fail_attempts: int,
    content: str,
    error_msg: str = "Temporary disk I/O error",
) -> tuple[Callable[[str], str], Callable[[], int]]:
    attempts = 0

    def read_file(filepath: str) -> str:
        nonlocal attempts
        attempts += 1
        if attempts <= fail_attempts:
            raise OSError(f"{error_msg} for {filepath} (attempt {attempts})")
        return content

    def get_attempts() -> int:
        return attempts

    return read_file, get_attempts


def make_token_registry(tokens: Iterable[str]) -> Callable[[str], bool]:
    allowed = frozenset(t.strip() for t in tokens if t.strip())
    return lambda token: token in allowed


def make_revocable_registry(
    tokens: Iterable[str],
) -> tuple[Callable[[str], bool], Callable[[str], None]]:
    allowed = set(tokens)

    def verify(token: str) -> bool:
        return token in allowed

    def revoke(token: str) -> None:
        allowed.discard(token)

    return verify, revoke
