from __future__ import annotations

from collections.abc import Iterable
from functools import partial, reduce
from operator import attrgetter, methodcaller
from typing import TypedDict

from models import Order, OrderRank


class OrderStats(TypedDict):
    count: int
    revenue: float
    avg_total: float
    max_total: float


get_total = attrgetter("total")
get_status = attrgetter("status")


def is_paid(order: Order) -> bool:
    status_val = str(get_status(order))
    return status_val.lower() == "paid"


def filter_paid_orders(orders: Iterable[Order]) -> list[Order]:
    return [o for o in orders if is_paid(o)]


def apply_discount_rate(order: Order, rate: float) -> Order:
    caller = methodcaller("discounted", rate)
    return caller(order)  # type: ignore[no-any-return]


make_standard_discount = partial(apply_discount_rate, rate=0.05)


def sort_and_rank_orders(orders: Iterable[Order], top_n: int = 5) -> list[Order]:
    ranked = sorted(
        [OrderRank(o) for o in orders],
        reverse=True,
    )
    return [r.order for r in ranked[:top_n]]


def calculate_orders_stats(orders: Iterable[Order]) -> OrderStats:
    order_list = list(orders)
    if not order_list:
        return {
            "count": 0,
            "revenue": 0.0,
            "avg_total": 0.0,
            "max_total": 0.0,
        }

    totals = [float(get_total(o)) for o in order_list]

    initial: tuple[int, float, float] = (0, 0.0, float("-inf"))

    def acc_fn(acc: tuple[int, float, float], val: float) -> tuple[int, float, float]:
        cnt, rev, max_t = acc
        return cnt + 1, round(rev + val, 2), max(max_t, val)

    count, revenue, max_val = reduce(acc_fn, totals, initial)
    avg_val = round(revenue / count, 2) if count > 0 else 0.0

    return {
        "count": count,
        "revenue": revenue,
        "avg_total": avg_val,
        "max_total": max_val,
    }


def process_orders_pipeline(
    orders: Iterable[Order],
    discount_rate: float = 0.05,
    top_n: int = 5,
) -> tuple[list[Order], OrderStats]:
    paid = filter_paid_orders(orders)
    discount_fn = partial(apply_discount_rate, rate=discount_rate)
    discounted = [discount_fn(o) for o in paid]
    top_orders = sort_and_rank_orders(discounted, top_n=top_n)
    stats = calculate_orders_stats(top_orders)
    return top_orders, stats
