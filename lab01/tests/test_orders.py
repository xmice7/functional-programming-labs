from core import (
    Order,
    OrderItem,
    order_subtotal,
    process_orders_pure,
    with_total,
)
from starter_imperative import process_orders as imperative_process_orders


def test_order_subtotal() -> None:
    items: list[OrderItem] = [{"price": 10.0, "qty": 2}, {"price": 5.0, "qty": 3}]
    assert order_subtotal(items) == 35.0


def test_with_total() -> None:
    order: Order = {"id": 1, "items": [], "paid": True}
    updated = with_total(order, 100.0)
    assert "total" not in order
    assert updated["total"] == 100.0


def test_process_orders_pure(sample_orders: list[Order]) -> None:
    res = process_orders_pure(sample_orders, min_total=50.0, discount=0.1, tax_rate=0.2)
    assert res["count"] == 1
    assert res["orders"][0]["total"] == 270.0
    assert res["revenue"] == 270.0


def test_orders_equivalence(sample_orders: list[Order]) -> None:
    imp_res = imperative_process_orders(sample_orders, min_total=50.0, discount=0.1)
    pure_res = process_orders_pure(
        sample_orders, min_total=50.0, discount=0.1, tax_rate=0.2
    )
    assert pure_res["count"] == imp_res["count"]
    assert pure_res["revenue"] == imp_res["revenue"]
