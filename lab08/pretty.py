from __future__ import annotations

from expr import Add, Div, Expr, Mul, Num, Sub


def pretty_expr(expr: Expr) -> str:
    match expr:
        case Num(val):
            return f"{val:g}"
        case Add(left, right):
            return f"({pretty_expr(left)} + {pretty_expr(right)})"
        case Sub(left, right):
            return f"({pretty_expr(left)} - {pretty_expr(right)})"
        case Mul(left, right):
            return f"({pretty_expr(left)} * {pretty_expr(right)})"
        case Div(left, right):
            return f"({pretty_expr(left)} / {pretty_expr(right)})"
