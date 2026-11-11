from __future__ import annotations

from core import add_service, calculate_total, extend_stay, update_status
from model import Booking, Guest


def main() -> None:
    guest = Guest(
        name="Олексій Корж",
        email="oleksiy@example.com",
        phone="+380501234567",
    )
    booking = Booking.create(
        booking_id=1001,
        guest=guest,
        room_number=305,
        nights=3,
        price_per_night=1200.0,
        status="confirmed",
        services=["breakfast"],
        meta={"source": "website", "vip": True},
    )

    print("Початкове бронювання:")
    print(f"ID: {booking.booking_id}, Гість: {booking.guest.name}")
    print(f"Ночей: {booking.nights}, Статус: {booking.status}")
    print(f"Послуги: {set(booking.services)}")

    prices = {"breakfast": 200.0, "spa": 500.0, "parking": 150.0}
    print(f"Базова вартість: {calculate_total(booking, prices)} грн")

    b_with_spa = add_service(booking, "spa")
    b_extended = extend_stay(b_with_spa, 2)
    b_final = update_status(b_extended, "checked_in")

    print("\nОновлене бронювання (нова копія):")
    print(f"Ночей: {b_final.nights}, Статус: {b_final.status}")
    print(f"Послуги: {set(b_final.services)}")
    print(f"Підсумкова вартість: {calculate_total(b_final, prices)} грн")

    print(
        f"\nНезмінність оригіналу: ночей={booking.nights}, "
        f"послуг={len(booking.services)}"
    )


if __name__ == "__main__":
    main()
