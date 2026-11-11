import pytest
from models import Order


@pytest.fixture
def sample_order_list() -> list[Order]:
    return [
        Order(1, "Іван", 1000.0, "paid", "Львів"),
        Order(2, "Марія", 500.0, "pending", "Київ"),
        Order(3, "Олег", 2500.0, "paid", "Львів"),
        Order(4, "Оксана", 1000.0, "paid", "Одеса"),
        Order(5, "Андрій", 800.0, "cancelled", "Дніпро"),
    ]
