# Лабораторна робота №2. Функції вищого порядку, lambda, композиція

**Варіант 6 — Рейтинг книг.**
Вхідні дані: книги (`id`, `title`, `genre`, `ratings`).
Конвеєр: обчислення середнього рейтингу, підсилення вибраного жанру, фільтрація за порогом, сортування за двома ключами та Top-N.
Reduce-агрегація: кількість, сума балів, середнє значення, min/max.
Виконав: Корж Олексій, група ФЕП-23.

## Як запускати

```bash
cd lab02
pip install -r requirements.txt
python app.py --top 5 --boost-genre Fantasy --factor 1.1 --min-rating 4.0
pytest -q
mypy --strict .
ruff check .
black --check .
```
