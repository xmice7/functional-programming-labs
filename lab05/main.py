from __future__ import annotations

from streams import drop, fib_stream, take
from transactions import (
    cumulative_balance,
    filter_positive,
    infinite_transaction_stream,
    moving_averages,
    moving_sums,
)


def main() -> None:
    raw_stream = infinite_transaction_stream()
    first_10_raw = list(take(10, raw_stream))
    print("Перші 10 транзакцій:", first_10_raw)

    pos_stream = filter_positive(infinite_transaction_stream())
    first_8_pos = list(take(8, pos_stream))
    print("Перші 8 додатних операцій:", first_8_pos)

    balance_stream = cumulative_balance(first_8_pos, initial_balance=500.0)
    print("Накопичувальний баланс:", list(balance_stream))

    window_size = 3
    sums_stream = moving_sums(first_8_pos, window_size)
    print(f"Перші ковзні суми (вікно {window_size}):", list(sums_stream))

    avg_stream = moving_averages(first_8_pos, window_size)
    print(f"Перші ковзні середні (вікно {window_size}):", list(avg_stream))

    dropped_pos = list(take(5, drop(3, filter_positive(infinite_transaction_stream()))))
    print("Пропуск перших 3 та вибір наступних 5 додатних:", dropped_pos)

    first_7_fib = list(take(7, fib_stream()))
    print("Лінивий стрім Фібоначчі (перші 7):", first_7_fib)


if __name__ == "__main__":
    main()
