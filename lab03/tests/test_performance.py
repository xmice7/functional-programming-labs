import time

from core import add_service, extend_stay
from model import Booking, Guest
from mutable_model import MutableBooking, MutableGuest


def test_performance_benchmark() -> None:
    iterations = 5000

    guest = Guest("Test", "t@example.com", "123")
    booking = Booking.create(1, guest, 101, 1, 100.0)

    start_immutable = time.perf_counter()
    curr_b = booking
    for i in range(iterations):
        curr_b = extend_stay(curr_b, 1)
        curr_b = add_service(curr_b, f"srv_{i % 10}")
    time_immutable = time.perf_counter() - start_immutable

    m_guest = MutableGuest("Test", "t@example.com", "123")
    m_booking = MutableBooking(1, m_guest, 101, 1, 100.0, "pending", [], {})

    start_mutable = time.perf_counter()
    for i in range(iterations):
        m_booking.extend_stay(1)
        m_booking.add_service(f"srv_{i % 10}")
    time_mutable = time.perf_counter() - start_mutable

    assert time_immutable > 0
    assert time_mutable > 0
    assert curr_b.nights == 1 + iterations
    assert m_booking.nights == 1 + iterations
