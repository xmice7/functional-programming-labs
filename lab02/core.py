from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import reduce
from typing import Any, TypedDict, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class BookRecord(TypedDict, total=False):
    id: int
    title: str
    genre: str
    ratings: list[float]
    avg_rating: float
    score: float


class Aggregation(TypedDict):
    count: int
    rating_sum: float
    avg_rating: float
    min_rating: float
    max_rating: float


def compute_avg_rating(book: BookRecord) -> BookRecord:
    ratings = book.get("ratings", [])
    avg = round(sum(ratings) / len(ratings), 3) if ratings else 0.0
    return {**book, "avg_rating": avg, "score": avg}


def boost_genre(book: BookRecord, target_genre: str, factor: float = 1.1) -> BookRecord:
    current_score = book.get("score", book.get("avg_rating", 0.0))
    if book.get("genre", "").lower() == target_genre.lower():
        boosted = round(min(5.0, current_score * factor), 3)
        return {**book, "score": boosted}
    return {**book, "score": current_score}


def filter_min_rating(
    books: Iterable[BookRecord], min_rating: float
) -> list[BookRecord]:
    return list(
        filter(
            lambda b: b.get("score", b.get("avg_rating", 0.0)) >= min_rating,
            books,
        )
    )


def sort_top_n(books: Iterable[BookRecord], n: int) -> list[BookRecord]:
    sorted_books = sorted(
        books,
        key=lambda b: (-b.get("score", 0.0), b.get("title", "")),
    )
    return sorted_books[:n]


def reduce_stats(books: Iterable[BookRecord]) -> Aggregation:
    book_list = list(books)
    if not book_list:
        return {
            "count": 0,
            "rating_sum": 0.0,
            "avg_rating": 0.0,
            "min_rating": 0.0,
            "max_rating": 0.0,
        }

    scores = [b.get("score", b.get("avg_rating", 0.0)) for b in book_list]

    initial: tuple[int, float, float, float] = (
        0,
        0.0,
        float("inf"),
        float("-inf"),
    )

    def accumulator(
        acc: tuple[int, float, float, float], score: float
    ) -> tuple[int, float, float, float]:
        cnt, r_sum, min_r, max_r = acc
        return (
            cnt + 1,
            round(r_sum + score, 3),
            min(min_r, score),
            max(max_r, score),
        )

    count, total_sum, min_val, max_val = reduce(accumulator, scores, initial)
    avg = round(total_sum / count, 3) if count > 0 else 0.0

    return {
        "count": count,
        "rating_sum": total_sum,
        "avg_rating": avg,
        "min_rating": min_val,
        "max_rating": max_val,
    }


def compose(
    f: Callable[[B], C],
    g: Callable[[A], B],
) -> Callable[[A], C]:
    return lambda x: f(g(x))


def pipe(value: A, *functions: Callable[[Any], Any]) -> Any:
    result = value
    for fn in functions:
        result = fn(result)
    return result


def process_books_pipeline(
    books: Iterable[BookRecord],
    *,
    boost_target_genre: str = "Fantasy",
    boost_factor: float = 1.1,
    min_rating: float = 4.0,
    top_n: int = 5,
) -> tuple[list[BookRecord], Aggregation]:
    step1 = list(map(compute_avg_rating, books))
    step2 = list(map(lambda b: boost_genre(b, boost_target_genre, boost_factor), step1))
    step3 = filter_min_rating(step2, min_rating)
    top_books = sort_top_n(step3, top_n)
    stats = reduce_stats(top_books)
    return top_books, stats
