from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from core import (
    DeliveryReport,
    Parcel,
    make_multiplier,
    pipe,
    process_parcels_pure,
    stamp_total,
)

SAMPLE_PARCELS: list[Parcel] = [
    {
        "id": 101,
        "weight": 2.5,
        "distance": 120.0,
        "delivery_type": "standard",
        "paid": True,
    },
    {
        "id": 102,
        "weight": 0.8,
        "distance": 45.0,
        "delivery_type": "express",
        "paid": True,
    },
    {
        "id": 103,
        "weight": 15.0,
        "distance": 350.0,
        "delivery_type": "same_day",
        "paid": False,
    },
    {
        "id": 104,
        "weight": 60.0,
        "distance": 80.0,
        "delivery_type": "standard",
        "paid": True,
    },
    {
        "id": 105,
        "weight": 5.0,
        "distance": 210.0,
        "delivery_type": "express",
        "paid": True,
    },
]


def render_delivery_report(report: DeliveryReport) -> str:
    header = (
        f"{'ID':<6} {'Вага(кг)':<10} {'Відстань(км)':<14} "
        f"{'Тип':<12} {'Вартість(грн)':<12}"
    )
    lines = [
        "=" * 60,
        "          ЗВІТ СИСТЕМИ ДОСТАВКИ (ВАРІАНТ 6)",
        "=" * 60,
        f"Опрацьовано валідних посилок: {report['count']}",
        f"Загальна вартість доставки:  {report['total_cost']:.2f} грн",
        "-" * 60,
        header,
        "-" * 60,
    ]
    for p in report["parcels"]:
        lines.append(
            f"{p['id']:<6} {p['weight']:<10.2f} {p['distance']:<14.1f} "
            f"{p['delivery_type']:<12} {p.get('cost', 0.0):<12.2f}"
        )
    lines.append("=" * 60)
    return "\n".join(lines)


def load_parcels(path: Path) -> list[Parcel]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return list(data)


def main() -> None:
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        parcels = load_parcels(file_path)
    else:
        parcels = SAMPLE_PARCELS

    report = process_parcels_pure(parcels, min_distance=10.0)
    print(render_delivery_report(report))

    stamped_total, timestamp = stamp_total(
        lambda: report["total_cost"],
        time.time,
    )
    print(f"\nЧасова мітка: {timestamp} (Total: {stamped_total})")

    mult_10 = make_multiplier(1.1)
    piped_val = pipe(100.0, mult_10, mult_10)
    print(f"pipe(100, *1.1, *1.1) = {piped_val:.2f}")


if __name__ == "__main__":
    main()
