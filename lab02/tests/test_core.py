import copy

from core import (
    BookRecord,
    boost_genre,
    compose,
    compute_avg_rating,
    pipe,
    process_books_pipeline,
    reduce_stats,
    sort_top_n,
)


def test_compute_avg_rating() -> None:
    book: BookRecord = {
        "id": 1,
        "title": "Test Book",
        "genre": "Fantasy",
        "ratings": [4.0, 5.0, 4.5],
    }
    updated = compute_avg_rating(book)
    assert updated["avg_rating"] == 4.5
    assert updated["score"] == 4.5
    assert "avg_rating" not in book


def test_boost_genre() -> None:
    book1: BookRecord = {
        "id": 1,
        "title": "Fantasy Book",
        "genre": "Fantasy",
        "score": 4.0,
    }
    boosted = boost_genre(book1, "Fantasy", factor=1.2)
    assert boosted["score"] == 4.8

    book2: BookRecord = {
        "id": 2,
        "title": "Tech Book",
        "genre": "Tech",
        "score": 4.0,
    }
    not_boosted = boost_genre(book2, "Fantasy", factor=1.2)
    assert not_boosted["score"] == 4.0


def test_immutability(sample_books: list[BookRecord]) -> None:
    backup = copy.deepcopy(sample_books)
    _ = process_books_pipeline(sample_books)
    assert sample_books == backup


def test_sort_top_n() -> None:
    books: list[BookRecord] = [
        {"id": 1, "title": "B Book", "score": 4.5},
        {"id": 2, "title": "A Book", "score": 4.5},
        {"id": 3, "title": "C Book", "score": 4.9},
    ]
    top2 = sort_top_n(books, 2)
    assert len(top2) == 2
    assert top2[0]["id"] == 3
    assert top2[1]["id"] == 2


def test_reduce_stats(sample_books: list[BookRecord]) -> None:
    processed = [compute_avg_rating(b) for b in sample_books]
    stats = reduce_stats(processed)
    assert stats["count"] == 5
    assert stats["rating_sum"] > 0
    assert stats["min_rating"] <= stats["avg_rating"] <= stats["max_rating"]


def test_reduce_stats_empty() -> None:
    stats = reduce_stats([])
    assert stats["count"] == 0
    assert stats["avg_rating"] == 0.0


def test_compose_and_pipe() -> None:
    def add_ten(x: float) -> float:
        return x + 10.0

    def multiply_two(x: float) -> float:
        return x * 2.0

    composed = compose(multiply_two, add_ten)
    assert composed(5.0) == 30.0

    assert pipe(5.0, add_ten, multiply_two) == 30.0


def test_pipeline_integration(sample_books: list[BookRecord]) -> None:
    top_books, stats = process_books_pipeline(
        sample_books,
        boost_target_genre="Fantasy",
        boost_factor=1.1,
        min_rating=4.0,
        top_n=3,
    )
    assert len(top_books) <= 3
    assert stats["count"] == len(top_books)
    for b in top_books:
        assert b.get("score", 0.0) >= 4.0
