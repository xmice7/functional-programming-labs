from __future__ import annotations

from typing import Any

from model import (
    Cancelled,
    Created,
    Delivered,
    InvalidStateTransitionError,
    OrderEvent,
    OrderState,
    Paid,
    Shipped,
)


def transition(
    state: OrderState,
    event: OrderEvent,
    **kwargs: Any,
) -> OrderState:
    match (state, event):
        case (Created(order_id, items), "pay"):
            tx_id = str(kwargs.get("transaction_id", f"tx_{order_id}"))
            paid_at = str(kwargs.get("timestamp", "2026-11-11T12:00:00Z"))
            return Paid(
                order_id=order_id,
                items=items,
                transaction_id=tx_id,
                paid_at=paid_at,
            )

        case (Created(order_id, items), "cancel"):
            reason = str(kwargs.get("reason", "Cancelled before payment"))
            cancelled_at = str(kwargs.get("timestamp", "2026-11-11T12:00:00Z"))
            return Cancelled(
                order_id=order_id,
                items=items,
                reason=reason,
                cancelled_at=cancelled_at,
            )

        case (Paid(order_id, items), "ship"):
            tracking = str(kwargs.get("tracking_code", f"TRK{order_id:06d}"))
            carrier = str(kwargs.get("carrier", "Nova Poshta"))
            shipped_at = str(kwargs.get("timestamp", "2026-11-11T14:00:00Z"))
            return Shipped(
                order_id=order_id,
                items=items,
                tracking_code=tracking,
                carrier=carrier,
                shipped_at=shipped_at,
            )

        case (Paid(order_id, items), "cancel"):
            reason = str(kwargs.get("reason", "Refund requested"))
            cancelled_at = str(kwargs.get("timestamp", "2026-11-11T12:30:00Z"))
            return Cancelled(
                order_id=order_id,
                items=items,
                reason=reason,
                cancelled_at=cancelled_at,
            )

        case (Shipped(order_id, items), "deliver"):
            delivered_at = str(kwargs.get("timestamp", "2026-11-12T10:00:00Z"))
            signed = str(kwargs.get("signed_by", "Олексій"))
            return Delivered(
                order_id=order_id,
                items=items,
                delivered_at=delivered_at,
                signed_by=signed,
            )

        case _:
            raise InvalidStateTransitionError(
                f"Invalid transition from '{state.status_name}' with '{event}'"
            )


def progress_percentage(state: OrderState) -> float:
    match state:
        case Created():
            return 10.0
        case Paid():
            return 40.0
        case Shipped():
            return 75.0
        case Delivered():
            return 100.0
        case Cancelled():
            return 0.0


def render_receipt(state: OrderState) -> str:
    lines = [
        f"Замовлення #{state.order_id} | Статус: {state.status_name}",
        f"Прогрес виконання: {progress_percentage(state):.0f}%",
        "Товари:",
    ]
    for it in state.items:
        lines.append(f"  - {it.name} (x{it.qty}): {it.subtotal:.2f} грн")
    lines.append(f"Всього до сплати: {state.total_amount:.2f} грн")

    match state:
        case Paid(_, _, tx_id, p_at):
            lines.append(f"Оплата успішна: транзакція {tx_id} о {p_at}")
        case Shipped(_, _, trk, carrier, s_at):
            lines.append(f"Відправлено: {carrier}, ТТН {trk} о {s_at}")
        case Delivered(_, _, d_at, signed):
            lines.append(f"Доставлено о {d_at}, отримав: {signed}")
        case Cancelled(_, _, reason, c_at):
            lines.append(f"Скасовано о {c_at}. Причина: {reason}")
        case Created():
            lines.append("Очікує оплати.")

    return "\n".join(lines)
