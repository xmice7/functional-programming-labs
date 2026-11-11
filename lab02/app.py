from __future__ import annotations

import argparse
import json
from pathlib import Path

from core import Aggregation, BookRecord, process_books_pipeline


def load_books(path: Path) -> list[BookRecord]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return list(data)


def render_results(books: list[BookRecord], stats: Aggregation) -> str:
    lines = [
        "=" * 65,
        "              РЕЙТИНГ КНИГ — ВАРІАНТ 6",
        "=" * 65,
        f"{'ID':<4} {'Назва книги':<35} {'Жанр':<12} {'Бал':<6}",
        "-" * 65,
    ]
    for b in books:
        title = b["title"][:33]
        score = b.get("score", 0.0)
        lines.append(f"{b['id']:<4} {title:<35} {b['genre']:<12} {score:<6.2f}")
    lines.append("-" * 65)
    lines.append("СТАТИСТИКА (REDUCE):")
    lines.append(f"  Кількість у вибірці: {stats['count']}")
    lines.append(f"  Сума балів:          {stats['rating_sum']:.2f}")
    lines.append(f"  Середній рейтинг:    {stats['avg_rating']:.2f}")
    lines.append(f"  Мінімальний бал:     {stats['min_rating']:.2f}")
    lines.append(f"  Максимальний бал:    {stats['max_rating']:.2f}")
    lines.append("=" * 65)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=Path("sample_data.json"))
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--boost-genre", type=str, default="Fantasy")
    parser.add_argument("--factor", type=float, default=1.1)
    parser.add_argument("--min-rating", type=float, default=4.0)

    args = parser.parse_args()

    books = load_books(args.file)
    top_books, stats = process_books_pipeline(
        books,
        boost_target_genre=args.boost_genre,
        boost_factor=args.factor,
        min_rating=args.min_rating,
        top_n=args.top,
    )
    print(render_results(top_books, stats))


if __name__ == "__main__":
    main()
