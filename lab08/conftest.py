import pytest
from model import Created, OrderItem


@pytest.fixture
def sample_created_order() -> Created:
    return Created(
        order_id=1,
        items=(
            OrderItem(name="Клавіатура", price=1200.0, qty=1),
            OrderItem(name="Килимок", price=300.0, qty=2),
        ),
        created_at="2026-11-11T09:00:00Z",
    )
