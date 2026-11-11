# Лабораторна робота №1. Основи функціонального програмування у Python

**Варіант 6 — Система доставки.**
Вхідні дані: посилки: вага (`weight`), відстань (`distance`), тип доставки (`delivery_type`), статус оплати (`paid`).
Розрахунок вартості доставки та надбавки. Тариф, надбавка і критерій прийнятності — через `typing.Callable`.
Виконав: Корж Олексій, група ФЕП-23.

## Цілі

- зрозуміти, що таке чиста функція і референтна прозорість;
- виявити та ізолювати побічні ефекти (print, глобальні константи `BASE_RATE_PER_KG` / `SURCHARGE_MAP`, мутація вхідних словників);
- переписати імперативний фрагмент `starter_imperative.py` у функціональному стилі;
- параметризувати обчислення через `typing.Callable` (тариф, надбавка, критерій прийнятності);
- реалізувати композицію функцій (`compose`, `pipe`), фабрики функцій (`make_multiplier`) та інжекцію годинника (`stamp_total`).

## Що зроблено

| Файл | Призначення |
|---|---|
| `core.py` | Чисте ядро варіанта 6: типи `Parcel`, `DeliveryReport`, `calc_base_tariff`, `calc_delivery_cost`, `with_delivery_cost`, фабрика `make_delivery_processor`, фабрики політик `linear_tariff_policy`, `table_surcharge_policy`, `standard_accept_policy`, `process_parcels_pure`. Додаткові методичні функції: `compose`, `pipe`, `make_multiplier`, `stamp_total`. Базове завдання: `order_subtotal`, `with_total`, `make_processor`, `process_orders_pure`. |
| `app.py` | Оболонка побічних ефектів: зчитування з JSON, форматування `render_delivery_report`, CLI виклик, `time.time`. |
| `starter_imperative.py` | Початковий імперативний код для перевірки еквівалентності бізнес-результатів. |
| `tests/test_core.py` | Pytest для варіанта 6: референтна прозорість, відсутність мутацій, еквівалентність, Callable-політики, compose/pipe. |
| `tests/test_orders.py` | Pytest для базового завдання з методички (замовлення). |
| `tests/test_properties.py` | Property-based тести (Hypothesis) на інваріанти та референтну прозорість. |
| `conftest.py` | Спільні фікстури `sample_parcels` та `sample_orders`. |

## Як запускати

```bash
cd lab01
pip install -r requirements.txt
python app.py
pytest -q
mypy --strict .
ruff check .
black --check .
```
