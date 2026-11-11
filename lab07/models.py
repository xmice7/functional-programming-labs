from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import Any


@dataclass(frozen=True, slots=True)
class Order:
    id: int
    customer: str
    total: float
    status: str
    city: str

    def discounted(self, pct: float) -> Order:
        new_total = round(max(0.0, self.total * (1.0 - pct)), 2)
        return Order(
            id=self.id,
            customer=self.customer,
            total=new_total,
            status=self.status,
            city=self.city,
        )


@total_ordering
class OrderRank:
    def __init__(self, order: Order) -> None:
        self.order = order

    @property
    def total(self) -> float:
        return self.order.total

    @property
    def order_id(self) -> int:
        return self.order.id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OrderRank):
            return NotImplemented
        return (self.total, self.order_id) == (other.total, other.order_id)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, OrderRank):
            return NotImplemented
        if self.total != other.total:
            return self.total < other.total
        return self.order_id > other.order_id

    def __repr__(self) -> str:
        return f"OrderRank(id={self.order_id}, total={self.total})"
