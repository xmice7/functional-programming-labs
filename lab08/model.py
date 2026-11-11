from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias


class InvalidStateTransitionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class OrderItem:
    name: str
    price: float
    qty: int

    @property
    def subtotal(self) -> float:
        return self.price * self.qty


@dataclass(frozen=True, slots=True)
class Created:
    order_id: int
    items: tuple[OrderItem, ...]
    created_at: str

    @property
    def status_name(self) -> str:
        return "Created"

    @property
    def can_cancel(self) -> bool:
        return True

    @property
    def total_amount(self) -> float:
        return sum(it.subtotal for it in self.items)


@dataclass(frozen=True, slots=True)
class Paid:
    order_id: int
    items: tuple[OrderItem, ...]
    transaction_id: str
    paid_at: str

    @property
    def status_name(self) -> str:
        return "Paid"

    @property
    def can_cancel(self) -> bool:
        return True

    @property
    def total_amount(self) -> float:
        return sum(it.subtotal for it in self.items)


@dataclass(frozen=True, slots=True)
class Shipped:
    order_id: int
    items: tuple[OrderItem, ...]
    tracking_code: str
    carrier: str
    shipped_at: str

    @property
    def status_name(self) -> str:
        return "Shipped"

    @property
    def can_cancel(self) -> bool:
        return False

    @property
    def total_amount(self) -> float:
        return sum(it.subtotal for it in self.items)


@dataclass(frozen=True, slots=True)
class Delivered:
    order_id: int
    items: tuple[OrderItem, ...]
    delivered_at: str
    signed_by: str

    @property
    def status_name(self) -> str:
        return "Delivered"

    @property
    def can_cancel(self) -> bool:
        return False

    @property
    def total_amount(self) -> float:
        return sum(it.subtotal for it in self.items)


@dataclass(frozen=True, slots=True)
class Cancelled:
    order_id: int
    items: tuple[OrderItem, ...]
    reason: str
    cancelled_at: str

    @property
    def status_name(self) -> str:
        return "Cancelled"

    @property
    def can_cancel(self) -> bool:
        return False

    @property
    def total_amount(self) -> float:
        return sum(it.subtotal for it in self.items)


OrderState: TypeAlias = Created | Paid | Shipped | Delivered | Cancelled

OrderEvent: TypeAlias = Literal["pay", "ship", "deliver", "cancel"]


class OrderStateProtocol(Protocol):
    order_id: int
    items: tuple[OrderItem, ...]
    status_name: str
    can_cancel: bool
    total_amount: float
