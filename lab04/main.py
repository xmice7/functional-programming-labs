from __future__ import annotations

import sys
import time

from algorithms import fib_memoized, fib_naive, quicksort_hybrid
from nested import (
    iterative_max_depth,
    iterative_nested_stats,
    max_depth,
    nested_count,
    nested_stats,
    nested_sum,
)


def main() -> None:
    data = [1, [2, 3], (4, [5, (6, 7)]), [8, [9, [10]]]]

    print("Вхідна вкладена структура:", data)
    print("nested_sum:", nested_sum(data))
    print("nested_count:", nested_count(data))
    s, c = nested_stats(data)
    print(f"nested_stats (рекурсивно): сума={s}, к-сть={c}")

    it_s, it_c = iterative_nested_stats(data)
    print(f"iterative_nested_stats:   сума={it_s}, к-сть={it_c}")

    print("max_depth (рекурсивно):", max_depth(data))
    print("iterative_max_depth:   ", iterative_max_depth(data))

    fib_memoized.cache_clear()
    t0 = time.perf_counter()
    res_m = fib_memoized(32)
    tm = time.perf_counter() - t0
    info = fib_memoized.cache_info()
    print(f"\nfib_memoized(32) = {res_m} за {tm:.6f}s | CacheInfo: {info}")

    t0 = time.perf_counter()
    res_n = fib_naive(32)
    tn = time.perf_counter() - t0
    print(f"fib_naive(32)    = {res_n} за {tn:.6f}s (прискорення: {tn / tm:.1f}x)")

    sample_list = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("\nquicksort_hybrid:", quicksort_hybrid(sample_list))
    print("Поточний ліміт стеку Python:", sys.getrecursionlimit())


if __name__ == "__main__":
    main()
