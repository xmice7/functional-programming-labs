import pytest
from evaluator import progress_percentage, render_receipt, transition
from model import (
    Cancelled,
    Created,
    Delivered,
    InvalidStateTransitionError,
    Paid,
    Shipped,
)


def test_full_successful_order_lifecycle(sample_created_order: Created) -> None:
    assert sample_created_order.can_cancel is True
    assert progress_percentage(sample_created_order) == 10.0

    paid = transition(sample_created_order, "pay", transaction_id="tx_123")
    assert isinstance(paid, Paid)
    assert paid.transaction_id == "tx_123"
    assert paid.can_cancel is True
    assert progress_percentage(paid) == 40.0

    shipped = transition(paid, "ship", tracking_code="TRK100", carrier="Meest")
    assert isinstance(shipped, Shipped)
    assert shipped.tracking_code == "TRK100"
    assert shipped.can_cancel is False
    assert progress_percentage(shipped) == 75.0

    delivered = transition(shipped, "deliver", signed_by="Олексій")
    assert isinstance(delivered, Delivered)
    assert delivered.signed_by == "Олексій"
    assert delivered.can_cancel is False
    assert progress_percentage(delivered) == 100.0


def test_cancellation_from_created(sample_created_order: Created) -> None:
    cancelled = transition(sample_created_order, "cancel", reason="Changed mind")
    assert isinstance(cancelled, Cancelled)
    assert cancelled.reason == "Changed mind"
    assert cancelled.can_cancel is False
    assert progress_percentage(cancelled) == 0.0


def test_cancellation_from_paid(sample_created_order: Created) -> None:
    paid = transition(sample_created_order, "pay", transaction_id="tx_99")
    cancelled = transition(paid, "cancel", reason="Refund requested")
    assert isinstance(cancelled, Cancelled)
    assert cancelled.reason == "Refund requested"


def test_invalid_transitions(sample_created_order: Created) -> None:
    with pytest.raises(InvalidStateTransitionError):
        transition(sample_created_order, "ship")

    with pytest.raises(InvalidStateTransitionError):
        transition(sample_created_order, "deliver")

    paid = transition(sample_created_order, "pay")
    with pytest.raises(InvalidStateTransitionError):
        transition(paid, "deliver")

    shipped = transition(paid, "ship")
    with pytest.raises(InvalidStateTransitionError):
        transition(shipped, "cancel")

    delivered = transition(shipped, "deliver")
    with pytest.raises(InvalidStateTransitionError):
        transition(delivered, "cancel")


def test_render_receipt(sample_created_order: Created) -> None:
    receipt = render_receipt(sample_created_order)
    assert "Замовлення #1" in receipt
    assert "Клавіатура" in receipt
    assert "1800.00" in receipt
