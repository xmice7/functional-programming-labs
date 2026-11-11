from __future__ import annotations

from eval_ import eval_expr
from evaluator import render_receipt, transition
from expr import Add, Mul, Num
from model import Created, OrderItem
from pretty import pretty_expr


def main() -> None:
    items = (
        OrderItem(name="Ноутбук", price=25000.0, qty=1),
        OrderItem(name="Мишка бездротова", price=850.0, qty=2),
    )

    state1 = Created(order_id=501, items=items, created_at="2026-11-11T10:00:00Z")
    print("=== ПОЧАТКОВИЙ СТАН ===")
    print(render_receipt(state1))

    state2 = transition(
        state1, "pay", transaction_id="TX_998877", timestamp="2026-11-11T10:15:00Z"
    )
    state3 = transition(
        state2, "ship", tracking_code="20450012345678", carrier="Нова Пошта"
    )
    state4 = transition(state3, "deliver", signed_by="Олексій Корж")

    print("\n=== ФІНАЛЬНИЙ СТАН ДОСТАВКИ ===")
    print(render_receipt(state4))

    math_tree = Mul(Add(Num(10), Num(5)), Num(2))
    print("\n=== АЛГЕБРАЇЧНІ ВИРАЗИ EXPR ===")
    print("Вираз:     ", pretty_expr(math_tree))
    print("Результат: ", eval_expr(math_tree))


if __name__ == "__main__":
    main()
