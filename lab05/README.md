# Лабораторна робота №5. Ліниві обчислення: генератори та itertools

**Варіант 6 — Потік фінансових транзакцій.**
Лінивий потік сум транзакцій: фільтрація додатних операцій, накопичувальний баланс, перші N ковзних сум та середніх.
Інструменти: `generator expression`, `accumulate`, `islice`, `sliding_window`, `take`, `drop`.
Виконав: Корж Олексій, група ФЕП-23.

## Як запускати

```bash
cd lab05
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
ruff check .
black --check .
```
