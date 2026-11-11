import copy
from collections.abc import Sequence

from core import process_orders_pipeline
from hypothesis import given
from hypothesis import strategies as st
from models import Order

order_strategy = st.builds(
    Order,
    id=st.integers(min_value=1, max_value=10000),
    customer=st.text(min_size=1, max_size=20),
    total=st.floats(
        min_value=10.0, max_value=10000.0, allow_nan=False, allow_infinity=False
    ),
    status=st.sampled_from(["paid", "pending", "cancelled"]),
    city=st.sampled_from(["Львів", "Київ", "Одеса", "Харків"]),
)


@given(st.lists(order_strategy, min_size=0, max_size=20))
def test_property_no_mutation(orders: Sequence[Order]) -> None:
    snapshot = copy.deepcopy(list(orders))
    _ = process_orders_pipeline(orders)
    assert orders == snapshot


@given(st.lists(order_strategy, min_size=0, max_size=20))
def test_property_invariants(orders: Sequence[Order]) -> None:
    top_orders, stats = process_orders_pipeline(orders, top_n=5)
    assert len(top_orders) <= 5
    assert stats["count"] == len(top_orders)
    if stats["count"] > 0:
        assert stats["revenue"] >= 0.0
        assert stats["avg_total"] <= stats["max_total"]
        for o in top_orders:
            assert o.status.lower() == "paid"
