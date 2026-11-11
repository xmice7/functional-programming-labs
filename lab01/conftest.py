import pytest
from core import Order, Parcel


@pytest.fixture
def sample_parcels() -> list[Parcel]:
    return [
        {
            "id": 1,
            "weight": 2.0,
            "distance": 100.0,
            "delivery_type": "standard",
            "paid": True,
        },
        {
            "id": 2,
            "weight": 5.0,
            "distance": 50.0,
            "delivery_type": "express",
            "paid": True,
        },
        {
            "id": 3,
            "weight": 1.0,
            "distance": 20.0,
            "delivery_type": "same_day",
            "paid": False,
        },
        {
            "id": 4,
            "weight": 70.0,
            "distance": 10.0,
            "delivery_type": "standard",
            "paid": True,
        },
    ]


@pytest.fixture
def sample_orders() -> list[Order]:
    return [
        {
            "id": 1,
            "items": [{"price": 100.0, "qty": 2}, {"price": 50.0, "qty": 1}],
            "paid": True,
        },
        {
            "id": 2,
            "items": [{"price": 20.0, "qty": 1}],
            "paid": True,
        },
        {
            "id": 3,
            "items": [{"price": 500.0, "qty": 1}],
            "paid": False,
        },
    ]
