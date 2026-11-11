from __future__ import annotations

from closures import make_file_simulator, make_logger
from decorators import call_stats, retries, timed


def main() -> None:
    logger, get_logs, _ = make_logger()

    simulated_reader, get_attempts = make_file_simulator(
        fail_attempts=2,
        content='{"status": "success", "payload": "data_chunk_42"}',
    )

    logged_times: list[tuple[str, float]] = []

    def sink(fn_name: str, elapsed: float) -> None:
        logged_times.append((fn_name, elapsed))

    clock = 100.0

    def fake_clock() -> float:
        nonlocal clock
        clock += 0.05
        return clock

    sleeps: list[float] = []

    def fake_sleep(d: float) -> None:
        sleeps.append(d)

    @call_stats(clock_fn=fake_clock)
    @timed(sink=sink, clock_fn=fake_clock)
    @retries(
        max_attempts=4,
        delay=0.1,
        backoff=2.0,
        exceptions=(OSError,),
        sleep_fn=fake_sleep,
        logger=logger,
    )
    def fetch_file(path: str) -> str:
        return simulated_reader(path)

    print("Запуск операції читання файлу...")
    result = fetch_file("/var/data/input.json")
    print("Результат читання:", result)
    print("Всього спроб файлового симулятора:", get_attempts())
    print("Зафіксовані затримки (sleep):", sleeps)
    print("Логи замикання-логера:")
    for log_msg in get_logs():
        print("  -", log_msg)

    stats = fetch_file.stats
    print(
        f"\nСтатистика викликів: {stats.total_calls} всього, "
        f"{stats.successes} успіхів, {stats.failures} помилок"
    )


if __name__ == "__main__":
    main()
