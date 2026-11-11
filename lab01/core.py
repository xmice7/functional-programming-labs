from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import TypedDict, TypeVar


class Parcel(TypedDict, total=False):
    id: int
    weight: float
    distance: float
    delivery_type: str
    paid: bool
    cost: float


class DeliveryReport(TypedDict):
    count: int
    total_cost: float
    parcels: list[Parcel]


TariffFn = Callable[[float, float], float]
SurchargeFn = Callable[[str], float]
AcceptFn = Callable[[Parcel], bool]
DeliveryProcessor = Callable[[Iterable[Parcel]], DeliveryReport]
NowFn = Callable[[], float]

A = TypeVar("A")


def calc_base_tariff(
    weight: float, distance: float, per_kg: float = 12.0, per_km: float = 2.5
) -> float:
    return (weight * per_kg) + (distance * per_km)


def calc_delivery_cost(
    weight: float,
    distance: float,
    delivery_type: str,
    tariff_fn: TariffFn,
    surcharge_fn: SurchargeFn,
) -> float:
    base = tariff_fn(weight, distance)
    surcharge = surcharge_fn(delivery_type)
    return round(base * surcharge, 2)


def with_delivery_cost(parcel: Parcel, cost: float) -> Parcel:
    return {**parcel, "cost": cost}


def make_delivery_processor(
    *,
    accept: AcceptFn,
    tariff_fn: TariffFn,
    surcharge_fn: SurchargeFn,
) -> DeliveryProcessor:
    def process(parcels: Iterable[Parcel]) -> DeliveryReport:
        qualified = [
            with_delivery_cost(
                p,
                calc_delivery_cost(
                    p["weight"],
                    p["distance"],
                    p["delivery_type"],
                    tariff_fn,
                    surcharge_fn,
                ),
            )
            for p in parcels
            if p.get("paid", False) and accept(p)
        ]
        total = round(sum(p["cost"] for p in qualified), 2)
        return {
            "count": len(qualified),
            "total_cost": total,
            "parcels": qualified,
        }

    return process


def linear_tariff_policy(per_kg: float = 12.0, per_km: float = 2.5) -> TariffFn:
    return lambda w, d: (w * per_kg) + (d * per_km)


def table_surcharge_policy(
    table: Mapping[str, float], default: float = 1.0
) -> SurchargeFn:
    return lambda delivery_type: table.get(delivery_type, default)


def standard_accept_policy(
    min_distance: float = 0.0,
    min_weight: float = 0.1,
    max_weight: float = 50.0,
) -> AcceptFn:
    return (
        lambda p: p["distance"] >= min_distance
        and min_weight <= p["weight"] <= max_weight
    )


def process_parcels_pure(
    parcels: Iterable[Parcel],
    *,
    min_distance: float = 0.0,
    per_kg: float = 12.0,
    per_km: float = 2.5,
    surcharges: Mapping[str, float] | None = None,
) -> DeliveryReport:
    table = (
        surcharges
        if surcharges is not None
        else {"standard": 1.0, "express": 1.35, "same_day": 1.75}
    )
    processor = make_delivery_processor(
        accept=standard_accept_policy(min_distance=min_distance),
        tariff_fn=linear_tariff_policy(per_kg=per_kg, per_km=per_km),
        surcharge_fn=table_surcharge_policy(table),
    )
    return processor(parcels)


def compose(*functions: Callable[[float], float]) -> Callable[[float], float]:
    def composed(x: float) -> float:
        result = x
        for fn in reversed(functions):
            result = fn(result)
        return result

    return composed


def pipe(value: A, *functions: Callable[[A], A]) -> A:
    result = value
    for fn in functions:
        result = fn(result)
    return result


def make_multiplier(factor: float) -> Callable[[float], float]:
    return lambda x: x * factor


def stamp_total(
    calc_fn: Callable[..., float],
    clock_fn: NowFn,
    *args: float,
) -> tuple[float, float]:
    total = calc_fn(*args)
    timestamp = clock_fn()
    return total, timestamp


class OrderItem(TypedDict):
    price: float
    qty: int


class Order(TypedDict, total=False):
    id: int
    items: list[OrderItem]
    paid: bool
    total: float


class OrderReport(TypedDict):
    count: int
    revenue: float
    orders: list[Order]


OrderFilterFn = Callable[[float], bool]
TransformFn = Callable[[float], float]
OrderProcessor = Callable[[Iterable[Order]], OrderReport]


def order_subtotal(items: Iterable[OrderItem]) -> float:
    return sum(item["price"] * item["qty"] for item in items)


def with_total(order: Order, total: float) -> Order:
    return {**order, "total": total}


def make_processor(
    *,
    accept: OrderFilterFn,
    apply_discount: TransformFn,
    apply_tax: TransformFn,
) -> OrderProcessor:
    def process(orders: Iterable[Order]) -> OrderReport:
        qualified: list[Order] = []
        for o in orders:
            if not o.get("paid", False):
                continue
            subtotal = order_subtotal(o["items"])
            if not accept(subtotal):
                continue
            final_total = apply_tax(apply_discount(subtotal))
            qualified.append(with_total(o, final_total))
        return {
            "count": len(qualified),
            "revenue": sum(o["total"] for o in qualified),
            "orders": qualified,
        }

    return process


def process_orders_pure(
    orders: Iterable[Order],
    min_total: float,
    discount: float,
    tax_rate: float = 0.2,
) -> OrderReport:
    proc = make_processor(
        accept=lambda total: total >= min_total,
        apply_discount=lambda total: total * (1 - discount),
        apply_tax=lambda total: total * (1 + tax_rate),
    )
    return proc(orders)
