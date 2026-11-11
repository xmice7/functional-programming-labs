from eval_ import eval_expr
from expr import Add, Expr, Num, Sub
from hypothesis import given
from hypothesis import strategies as st
from model import Created, OrderItem


def expr_strategy() -> st.SearchStrategy[Expr]:
    leaf = st.builds(
        Num,
        st.floats(
            min_value=-1000.0,
            max_value=1000.0,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    return st.recursive(
        leaf,
        lambda children: st.builds(Add, children, children)
        | st.builds(Sub, children, children),
        max_leaves=10,
    )


@given(expr_strategy())
def test_property_expr_evaluation(e: Expr) -> None:
    res1 = eval_expr(e)
    res2 = eval_expr(e)
    assert res1 == res2


@given(
    st.lists(
        st.builds(
            OrderItem,
            name=st.text(min_size=1, max_size=10),
            price=st.floats(
                min_value=1.0,
                max_value=500.0,
                allow_nan=False,
                allow_infinity=False,
            ),
            qty=st.integers(min_value=1, max_value=5),
        ),
        min_size=1,
        max_size=5,
    )
)
def test_property_order_total(items: list[OrderItem]) -> None:
    order = Created(1, tuple(items), "2026-11-11T00:00:00Z")
    expected = sum(it.price * it.qty for it in items)
    assert abs(order.total_amount - expected) < 1e-4
