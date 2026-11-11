from __future__ import annotations

from dataclasses import replace
from types import MappingProxyType
from typing import Any

from model import Booking


def add_service(booking: Booking, service: str) -> Booking:
    new_services = booking.services | {service}
    return replace(booking, services=new_services)


def update_status(booking: Booking, new_status: str) -> Booking:
    return replace(booking, status=new_status)


def extend_stay(booking: Booking, additional_nights: int) -> Booking:
    if additional_nights < 0:
        raise ValueError("additional_nights must be non-negative")
    return replace(booking, nights=booking.nights + additional_nights)


def update_meta(booking: Booking, key: str, value: Any) -> Booking:
    current = dict(booking.meta)
    current[key] = value
    return replace(booking, meta=MappingProxyType(current))


def calculate_total(
    booking: Booking, service_prices: dict[str, float] | None = None
) -> float:
    base = booking.nights * booking.price_per_night
    if not service_prices:
        return round(base, 2)
    services_cost = sum(service_prices.get(srv, 0.0) for srv in booking.services)
    return round(base + services_cost, 2)
