from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable
from functools import singledispatch
from pathlib import Path
from typing import Any

from models import Order


def _dict_to_order(d: dict[str, Any]) -> Order:
    return Order(
        id=int(d["id"]),
        customer=str(d["customer"]),
        total=float(d["total"]),
        status=str(d["status"]),
        city=str(d["city"]),
    )


def parse_json_orders(content: str) -> list[Order]:
    data = json.loads(content)
    return [_dict_to_order(item) for item in data]


def parse_csv_orders(content: str) -> list[Order]:
    reader = csv.DictReader(io.StringIO(content.strip()))
    return [_dict_to_order(row) for row in reader]


@singledispatch
def load_orders(source: Any) -> list[Order]:
    raise TypeError(f"Unsupported source type: {type(source).__name__}")


@load_orders.register(str)
def _load_from_str(source: str) -> list[Order]:
    trimmed = source.strip()
    if trimmed.startswith("[") or trimmed.startswith("{"):
        return parse_json_orders(trimmed)
    p = Path(trimmed)
    if p.exists() and p.is_file():
        return load_orders(p)
    if "customer" in trimmed and "total" in trimmed:
        return parse_csv_orders(trimmed)
    raise ValueError(f"Cannot parse string source: {source[:30]}...")


@load_orders.register(Path)
def _load_from_path(source: Path) -> list[Order]:
    content = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        return parse_json_orders(content)
    if source.suffix.lower() == ".csv":
        return parse_csv_orders(content)
    try:
        return parse_json_orders(content)
    except Exception:
        return parse_csv_orders(content)


@load_orders.register(io.TextIOBase)
def _load_from_textio(source: io.TextIOBase) -> list[Order]:
    content = source.read()
    try:
        return parse_json_orders(content)
    except Exception:
        return parse_csv_orders(content)


@load_orders.register(list)
@load_orders.register(tuple)
def _load_from_iterable(source: Iterable[Any]) -> list[Order]:
    result: list[Order] = []
    for item in source:
        if isinstance(item, Order):
            result.append(item)
        elif isinstance(item, dict):
            result.append(_dict_to_order(item))
        else:
            raise TypeError(f"Expected Order or dict, got {type(item).__name__}")
    return result
