# Лабораторна робота №7. functools та operator

**Варіант 6 — Замовлення інтернет-магазину.**
Модель: `Order`, `OrderRank` з `@total_ordering`.
Поліморфне завантаження через `@singledispatch` `load_orders` (str, Path, TextIO, list) для JSON та CSV форматів.
Функціональний конвеєр: фільтрація `paid` замовлень через `operator.attrgetter`, знижка через `functools.partial`, сортування та Top-N через `OrderRank`, статистика через `functools.reduce`.
Виконав: Корж Олексій, група ФЕП-23.

## Як запускати

```bash
cd lab07
pip install -r requirements.txt
python main.py --file sample_data.json --top 5 --discount 0.05
pytest -q
mypy --strict .
ruff check .
black --check .
```
