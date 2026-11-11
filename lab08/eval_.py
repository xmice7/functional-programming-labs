from __future__ import annotations

from expr import Add, Div, Expr, Mul, Num, Sub


def eval_expr(expr: Expr) -> float:
    match expr:
        case Num(val):
            return float(val)
        case Add(left, right):
            return eval_expr(left) + eval_expr(right)
        case Sub(left, right):
            return eval_expr(left) - eval_expr(right)
        case Mul(left, right):
            return eval_expr(left) * eval_expr(right)
        case Div(left, right):
            denominator = eval_expr(right)
            if denominator == 0.0:
                raise ZeroDivisionError("Division by zero in Expr")
            return eval_expr(left) / denominator
