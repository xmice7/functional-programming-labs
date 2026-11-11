from __future__ import annotations

from closures import make_counter, make_file_simulator, make_logger
from decorators import cached, call_stats, retries, timed

log = make_logger("app", print)
ticks = make_counter()


def fake_clock() -> float:
    return ticks() * 0.001


def fake_sleep(s: float) -> None:
    log(f"(sleep {s:.3f}s skipped)")


sim_read, sim_attempts = make_file_simulator(
    fail_attempts=2,
    content="Config payload line 1\nConfig payload line 2\n",
    error_msg="Simulated disk read timeout",
)


@call_stats(clock=fake_clock)
@timed("read_config_file", logger=log, clock=fake_clock)
@retries(attempts=4, delay=0.05, backoff=2.0, sleep=fake_sleep, logger=log)
def read_config_file(filepath: str) -> str:
    return sim_read(filepath)


@cached(ttl=30.0, time_fn=fake_clock)
def parse_config_metrics(raw_data: str) -> dict[str, int]:
    return {"lines": len(raw_data.splitlines()), "chars": len(raw_data)}


def main() -> None:
    print("Reading file with retries:")
    content = read_config_file("/etc/app/config.json")
    print("Content read successfully:\n", content)
    print("Simulated attempts:", sim_attempts())
    print("Stats total calls:", read_config_file.stats.total_calls)
    print("Stats successes:", read_config_file.stats.successes)
    print("Stats failures:", read_config_file.stats.failures)

    metrics = parse_config_metrics(content)
    print("Metrics:", metrics)
    print("Cache size:", parse_config_metrics.cache_size())


if __name__ == "__main__":
    main()
