# Лабораторна робота №3. Незмінні структури даних (immutability) у Python

**Варіант 6 — Бронювання готелю.**
Модель: `Booking`, `Guest`, `services`, `meta`.
Pure updates: `add_service`, `update_status`, `extend_stay` через `dataclasses.replace`.
Незмінність: `frozen dataclass`, `frozenset`, `MappingProxyType`.
Виконав: Корж Олексій, група ФЕП-23.

## Як запускати

```bash
cd lab03
pip install -r requirements.txt
python main.py
pytest -q
mypy --strict .
ruff check .
black --check .
```
