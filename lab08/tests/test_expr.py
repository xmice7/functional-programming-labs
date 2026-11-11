import pytest
from eval_ import eval_expr
from expr import Add, Div, Mul, Num, Sub
from pretty import pretty_expr


def test_eval_expr_basic() -> None:
    expr = Add(Num(5), Mul(Num(3), Num(4)))
    assert eval_expr(expr) == 17.0
    assert pretty_expr(expr) == "(5 + (3 * 4))"


def test_eval_expr_sub_div() -> None:
    expr = Div(Sub(Num(20), Num(5)), Num(3))
    assert eval_expr(expr) == 5.0
    assert pretty_expr(expr) == "((20 - 5) / 3)"


def test_zero_division() -> None:
    expr = Div(Num(10), Num(0))
    with pytest.raises(ZeroDivisionError):
        eval_expr(expr)
