from __future__ import annotations

from collections.abc import Callable


def make_logger() -> tuple[
    Callable[[str], None],
    Callable[[], list[str]],
    Callable[[], None],
]:
    logs: list[str] = []

    def log(msg: str) -> None:
        logs.append(msg)

    def get_logs() -> list[str]:
        return list(logs)

    def clear() -> None:
        logs.clear()

    return log, get_logs, clear


def make_call_counter() -> tuple[
    Callable[[], int],
    Callable[[], int],
    Callable[[], None],
]:
    count = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    def get_count() -> int:
        return count

    def reset() -> None:
        nonlocal count
        count = 0

    return increment, get_count, reset


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
