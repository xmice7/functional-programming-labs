# Лабораторна робота №6. Замикання та декоратори як HOF

**Варіант 6 — Повторні спроби файлової операції.**
Замикання: closure-логер (`make_logger`), замикання стану лічильника (`make_call_counter`), симулятор збоїв файлової системи (`make_file_simulator`).
Декоратори: `@retries` (експоненціальний backoff, підміна sleep та logger), `@call_stats`, `@timed`, `@cached_with_ttl`.
Збереження метаданих через `functools.wraps`, сувора типізація `ParamSpec` та `TypeVar`.
Виконав: Корж Олексій, група ФЕП-23.

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
