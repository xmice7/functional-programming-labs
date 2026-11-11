# Лабораторна робота №6. Замикання та декоратори як HOF

**Варіант 6 — Повторні спроби файлової операції.**
Замикання: `make_counter` (стан через nonlocal), `make_logger` (з інжектованим sink), симулятор збоїв файлової системи `make_file_simulator`, реєстри токенів.
Декоратори: `@retries` (експоненційний backoff, jitter, підміна sleep та logger), `@timed` (інжектовані clock/logger), `@cached` (TTL-кеш із `cache_clear` та `cache_invalidate`), `@call_stats` (збір статистики викликів).
Збереження метаданих через `functools.wraps`, повна типізація `ParamSpec` та `TypeVar`.
Виконав: Корж Олексій, група ФЕП-23.

## Структура файлів

- `closures.py`: реалізація замикань зі збереженням стану (`make_counter`, `make_logger`, `make_file_simulator`, `make_token_registry`, `make_revocable_registry`)
- `decorators.py`: параметризовані декоратори `@timed`, `@retries`, `@cached`, `@call_stats`
- `app.py`: демонстраційний сценарій імітації нестабільного читання файлу з повторними спробами та статистикою
- `tests/`: набір тестів pytest та Hypothesis (`test_closures.py`, `test_timed.py`, `test_retries.py`, `test_cached.py`, `test_stats.py`)

## Як запускати

```bash
cd lab06
pip install -r requirements.txt
python app.py
pytest -q
mypy --strict .
ruff check .
black --check .
```
