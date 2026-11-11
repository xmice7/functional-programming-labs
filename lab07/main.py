from __future__ import annotations

import argparse
from pathlib import Path

from core import process_orders_pipeline
from loaders import load_orders
from models import Order


def print_orders_table(orders: list[Order]) -> None:
    print(f"{'ID':<4} {'Клієнт':<20} {'Місто':<12} {'Сума (грн)':<12}")
    print("-" * 52)
    for o in orders:
        print(f"{o.id:<4} {o.customer:<20} {o.city:<12} {o.total:<12.2f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=Path("sample_data.json"))
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--discount", type=float, default=0.05)

    args = parser.parse_args()

    orders = load_orders(args.file)
    top_orders, stats = process_orders_pipeline(
        orders,
        discount_rate=args.discount,
        top_n=args.top,
    )

    print("=" * 52)
    print("      РЕЙТИНГ ОПЛАЧЕНИХ ЗАМОВЛЕНЬ (ВАРІАНТ 6)")
    print("=" * 52)
    print_orders_table(top_orders)
    print("=" * 52)
    print("СТАТИСТИКА (REDUCE):")
    print(f"  Кількість:     {stats['count']}")
    print(f"  Сумарний виторг: {stats['revenue']:.2f} грн")
    print(f"  Середній чек:   {stats['avg_total']:.2f} грн")
    print(f"  Максимальний чек: {stats['max_total']:.2f} грн")
    print("=" * 52)


if __name__ == "__main__":
    main()
