import pytest
from closures import make_call_counter, make_file_simulator, make_logger


def test_logger_closure() -> None:
    log, get_logs, clear = make_logger()
    assert get_logs() == []
    log("msg 1")
    log("msg 2")
    assert get_logs() == ["msg 1", "msg 2"]
    clear()
    assert get_logs() == []


def test_call_counter_closure() -> None:
    inc, get_cnt, reset = make_call_counter()
    assert get_cnt() == 0
    assert inc() == 1
    assert inc() == 2
    assert get_cnt() == 2
    reset()
    assert get_cnt() == 0


def test_file_simulator_closure() -> None:
    read_fn, get_attempts = make_file_simulator(2, "payload_ok")
    assert get_attempts() == 0

    with pytest.raises(OSError):
        read_fn("file.txt")
    assert get_attempts() == 1

    with pytest.raises(OSError):
        read_fn("file.txt")
    assert get_attempts() == 2

    assert read_fn("file.txt") == "payload_ok"
    assert get_attempts() == 3
