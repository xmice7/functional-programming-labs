# Функціональне програмування на Python — лабораторні роботи

Корж Олексій, ФЕП-23, варіант 6.

| Лабораторна | Тема | Варіант 6 |
|---|---|---|
| [lab01](lab01/) | Основи ФП: чисті функції, референтна прозорість, `typing.Callable` | Система доставки |
| [lab02](lab02/) | Функції вищого порядку, lambda, композиція: конвеєр map/filter/reduce | Рейтинг книг |
| [lab03](lab03/) | Незмінні структури даних: tuple, frozenset, frozen dataclass, MappingProxyType | Бронювання готелю |
| [lab04](lab04/) | Рекурсія та мемоізація: підрахунок суми та кількості вкладених чисел, quicksort, обходи дерев, lru_cache | Підрахунок суми вкладеної структури |
| [lab05](lab05/) | Ліниві обчислення: генератори та itertools: accumulate, islice, sliding_window | Потік фінансових транзакцій |
| [lab06](lab06/) | Замикання та декоратори як HOF: closure-логер, @retries, статистика викликів, @timed, @cached | Повторні спроби файлової операції |
| [lab07](lab07/) | functools та operator: partial, reduce, singledispatch, total_ordering | Замовлення інтернет-магазину |
| [lab08](lab08/) | Алгебраїчні типи даних: Union, Literal, Protocol, match/case | Стани замовлення |

Кожна `labN/` — самостійний проєкт: `README.md`, код, `tests/` (pytest + Hypothesis),
`requirements.txt` і звіт `report.pdf`. Стиль: `black`, `ruff`; типи: `mypy --strict`
(конфіг у `pyproject.toml`).

## Як запускати

Команди виконуються з каталогу конкретної лабораторної (модулі різних лаб мають
однакові імена, тому запуск pytest/mypy з кореня репозиторію не підтримується):

```bash
cd lab01
pip install -r requirements.txt
pytest -q
mypy --strict .
ruff check .
black --check .
```

Усі лаби одразу: `python check_all.py` з кореня репозиторію.
