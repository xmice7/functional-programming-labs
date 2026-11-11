from dataclasses import FrozenInstanceError

import pytest
from core import add_service, calculate_total, extend_stay, update_meta, update_status
from model import Booking, BookingKey, Guest


def test_frozen_attributes_cannot_be_mutated(sample_booking: Booking) -> None:
    with pytest.raises(FrozenInstanceError):
        sample_booking.status = "confirmed"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        sample_booking.nights = 5  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        sample_booking.guest.name = "New Name"  # type: ignore[misc]


def test_mapping_proxy_read_only(sample_booking: Booking) -> None:
    with pytest.raises(TypeError):
        sample_booking.meta["vip"] = True  # type: ignore[index]


def test_add_service_is_pure(sample_booking: Booking) -> None:
    updated = add_service(sample_booking, "breakfast")
    assert "breakfast" not in sample_booking.services
    assert "breakfast" in updated.services
    assert updated.booking_id == sample_booking.booking_id
    assert updated is not sample_booking


def test_update_status_is_pure(sample_booking: Booking) -> None:
    updated = update_status(sample_booking, "confirmed")
    assert sample_booking.status == "pending"
    assert updated.status == "confirmed"
    assert updated is not sample_booking


def test_extend_stay_is_pure(sample_booking: Booking) -> None:
    updated = extend_stay(sample_booking, 3)
    assert sample_booking.nights == 2
    assert updated.nights == 5
    assert updated is not sample_booking


def test_extend_stay_negative_error(sample_booking: Booking) -> None:
    with pytest.raises(ValueError):
        extend_stay(sample_booking, -1)


def test_update_meta_is_pure(sample_booking: Booking) -> None:
    updated = update_meta(sample_booking, "discount", 0.15)
    assert "discount" not in sample_booking.meta
    assert updated.meta["discount"] == 0.15
    assert updated is not sample_booking


def test_calculate_total(sample_booking: Booking) -> None:
    prices = {"wifi": 50.0, "spa": 300.0}
    total = calculate_total(sample_booking, prices)
    assert total == (2 * 1000.0 + 50.0)


def test_hashability_and_keys(sample_guest: Guest, sample_booking: Booking) -> None:
    guest_set = {sample_guest}
    assert sample_guest in guest_set

    key1 = sample_booking.key
    key2 = BookingKey(sample_booking.booking_id, sample_booking.room_number)
    assert hash(key1) == hash(key2)
    booking_dict = {key1: sample_booking}
    assert booking_dict[key2] == sample_booking

    with pytest.raises(TypeError):
        hash(sample_booking)
