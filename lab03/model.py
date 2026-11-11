from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class Guest:
    name: str
    email: str
    phone: str


@dataclass(frozen=True, slots=True)
class BookingKey:
    booking_id: int
    room_number: int


@dataclass(frozen=True, slots=True)
class Booking:
    booking_id: int
    guest: Guest
    room_number: int
    nights: int
    price_per_night: float
    status: str
    services: frozenset[str]
    meta: MappingProxyType[str, Any]

    @classmethod
    def create(
        cls,
        booking_id: int,
        guest: Guest,
        room_number: int,
        nights: int,
        price_per_night: float,
        status: str = "pending",
        services: Iterable[str] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> Booking:
        frozen_services = frozenset(services) if services else frozenset()
        proxy_meta = MappingProxyType(dict(meta)) if meta else MappingProxyType({})
        return cls(
            booking_id=booking_id,
            guest=guest,
            room_number=room_number,
            nights=nights,
            price_per_night=price_per_night,
            status=status,
            services=frozen_services,
            meta=proxy_meta,
        )

    @property
    def key(self) -> BookingKey:
        return BookingKey(self.booking_id, self.room_number)
