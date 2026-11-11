from __future__ import annotations

from typing import Any


def nested_sum(data: Any) -> float:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return float(data)
    if isinstance(data, (list, tuple)):
        return float(sum(nested_sum(item) for item in data))
    return 0.0


def nested_count(data: Any) -> int:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return 1
    if isinstance(data, (list, tuple)):
        return sum(nested_count(item) for item in data)
    return 0


def nested_stats(data: Any) -> tuple[float, int]:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return float(data), 1
    if isinstance(data, (list, tuple)):
        total_sum = 0.0
        total_count = 0
        for item in data:
            s, c = nested_stats(item)
            total_sum += s
            total_count += c
        return total_sum, total_count
    return 0.0, 0


def max_depth(data: Any) -> int:
    if not isinstance(data, (list, tuple)):
        return 0
    if not data:
        return 1
    return 1 + max(max_depth(item) for item in data)


def iterative_nested_stats(data: Any) -> tuple[float, int]:
    stack: list[Any] = [data]
    total_sum = 0.0
    count = 0

    while stack:
        curr = stack.pop()
        if isinstance(curr, (int, float)) and not isinstance(curr, bool):
            total_sum += float(curr)
            count += 1
        elif isinstance(curr, (list, tuple)):
            for item in reversed(curr):
                stack.append(item)

    return total_sum, count


def iterative_max_depth(data: Any) -> int:
    if not isinstance(data, (list, tuple)):
        return 0
    if not data:
        return 1

    stack: list[tuple[Any, int]] = [(data, 1)]
    max_d = 1

    while stack:
        curr, d = stack.pop()
        if d > max_d:
            max_d = d
        if isinstance(curr, (list, tuple)):
            for item in curr:
                if isinstance(item, (list, tuple)):
                    stack.append((item, d + 1))

    return max_d
