import io
from pathlib import Path

import pytest
from core import (
    calculate_orders_stats,
    make_standard_discount,
    process_orders_pipeline,
)
from loaders import load_orders
from models import Order, OrderRank


def test_order_rank_total_ordering() -> None:
    o1 = Order(1, "A", 1000.0, "paid", "Київ")
    o2 = Order(2, "B", 2000.0, "paid", "Львів")
    o3 = Order(3, "C", 1000.0, "paid", "Одеса")

    r1, r2, r3 = OrderRank(o1), OrderRank(o2), OrderRank(o3)

    assert r1 < r2
    assert r2 > r1
    assert r1 <= r2
    assert r2 >= r1
    assert r1 == OrderRank(Order(1, "A", 1000.0, "paid", "Київ"))

    assert r1 > r3
    assert r3 < r1

    assert (r1 == "not_a_rank") is False
    with pytest.raises(TypeError):
        _ = r1 < 123


def test_singledispatch_str_json() -> None:
    raw_json = (
        '[{"id": 10, "customer": "Test", '
        '"total": 100.0, "status": "paid", "city": "Київ"}]'
    )
    orders = load_orders(raw_json)
    assert len(orders) == 1
    assert orders[0].id == 10
    assert orders[0].total == 100.0


def test_singledispatch_str_csv() -> None:
    raw_csv = "id,customer,total,status,city\n11,Anna,300.0,paid,Львів\n"
    orders = load_orders(raw_csv)
    assert len(orders) == 1
    assert orders[0].id == 11
    assert orders[0].customer == "Anna"


def test_singledispatch_files(tmp_path: Path) -> None:
    json_file = tmp_path / "orders.json"
    json_file.write_text(
        '[{"id": 20, "customer": "Petro", "total": 500.0, '
        '"status": "paid", "city": "Львів"}]',
        encoding="utf-8",
    )
    from_path = load_orders(json_file)
    assert len(from_path) == 1
    assert from_path[0].id == 20

    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "id,customer,total,status,city\n21,Oleg,750.0,paid,Київ\n",
        encoding="utf-8",
    )
    from_csv_path = load_orders(csv_file)
    assert len(from_csv_path) == 1
    assert from_csv_path[0].id == 21


def test_singledispatch_textio() -> None:
    buf = io.StringIO("id,customer,total,status,city\n30,Dmytro,900.0,paid,Харків\n")
    orders = load_orders(buf)
    assert len(orders) == 1
    assert orders[0].id == 30


def test_singledispatch_list_collection(
    sample_order_list: list[Order],
) -> None:
    orders = load_orders(sample_order_list)
    assert len(orders) == len(sample_order_list)


def test_singledispatch_unsupported() -> None:
    with pytest.raises(TypeError):
        load_orders(12345)


def test_pipeline_processing(sample_order_list: list[Order]) -> None:
    top, stats = process_orders_pipeline(sample_order_list, discount_rate=0.1, top_n=2)
    assert len(top) == 2
    assert stats["count"] == 2
    assert top[0].total == 2250.0
    assert top[1].total == 900.0


def test_partial_discount() -> None:
    order = Order(1, "Test", 100.0, "paid", "Київ")
    discounted = make_standard_discount(order)
    assert discounted.total == 95.0


def test_empty_orders_stats() -> None:
    stats = calculate_orders_stats([])
    assert stats["count"] == 0
    assert stats["revenue"] == 0.0
