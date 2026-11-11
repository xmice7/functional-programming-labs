import pytest
from model import Booking, Guest


@pytest.fixture
def sample_guest() -> Guest:
    return Guest(
        name="Олексій Корж",
        email="oleksiy@example.com",
        phone="+380501234567",
    )


@pytest.fixture
def sample_booking(sample_guest: Guest) -> Booking:
    return Booking.create(
        booking_id=1,
        guest=sample_guest,
        room_number=101,
        nights=2,
        price_per_night=1000.0,
        status="pending",
        services=["wifi"],
        meta={"source": "mobile"},
    )
