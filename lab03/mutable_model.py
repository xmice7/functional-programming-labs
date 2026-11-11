from __future__ import annotations

from typing import Any


class MutableGuest:
    def __init__(self, name: str, email: str, phone: str) -> None:
        self.name = name
        self.email = email
        self.phone = phone


class MutableBooking:
    def __init__(
        self,
        booking_id: int,
        guest: MutableGuest,
        room_number: int,
        nights: int,
        price_per_night: float,
        status: str,
        services: list[str],
        meta: dict[str, Any],
    ) -> None:
        self.booking_id = booking_id
        self.guest = guest
        self.room_number = room_number
        self.nights = nights
        self.price_per_night = price_per_night
        self.status = status
        self.services = services
        self.meta = meta

    def add_service(self, service: str) -> None:
        self.services.append(service)

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    def extend_stay(self, additional_nights: int) -> None:
        self.nights += additional_nights
