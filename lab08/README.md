# Лабораторна робота №8. Алгебраїчні типи даних “по-Python’івськи”

**Варіант 6 — Стани замовлення.**
Алгебраїчні типи даних (sum types): `OrderState = Created | Paid | Shipped | Delivered | Cancelled`.
Події: `OrderEvent = Literal["pay", "ship", "deliver", "cancel"]`.
Контракт через `typing.Protocol`: `OrderStateProtocol`.
Чиста машина станів `transition(state, event)` через `match/case` із забороною некоректних переходів.
Базове дерево виразів методички: `Expr = Num | Add | Mul | Sub | Div` з чистим `eval_expr` та `pretty_expr`.
Сувора статична типізація: `mypy --strict`.
Виконав: Корж Олексій, група ФЕП-23.

## Як запускати

```bash
cd lab08
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
ruff check .
black --check .
```
