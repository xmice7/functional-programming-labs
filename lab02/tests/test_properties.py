import copy
from collections.abc import Sequence

from core import BookRecord, process_books_pipeline
from hypothesis import given
from hypothesis import strategies as st

book_strategy = st.fixed_dictionaries(
    {
        "id": st.integers(min_value=1, max_value=10000),
        "title": st.text(min_size=1, max_size=20),
        "genre": st.sampled_from(["Fantasy", "Sci-Fi", "Tech", "Classics"]),
        "ratings": st.lists(
            st.floats(
                min_value=1.0,
                max_value=5.0,
                allow_nan=False,
                allow_infinity=False,
            ),
            min_size=1,
            max_size=10,
        ),
    }
)


@given(st.lists(book_strategy, min_size=0, max_size=20))
def test_property_no_mutation(books: Sequence[BookRecord]) -> None:
    snapshot = copy.deepcopy(list(books))
    _ = process_books_pipeline(books)
    assert books == snapshot


@given(st.lists(book_strategy, min_size=0, max_size=20))
def test_property_invariants(books: Sequence[BookRecord]) -> None:
    top_books, stats = process_books_pipeline(books, top_n=5, min_rating=3.0)
    assert len(top_books) <= 5
    assert stats["count"] == len(top_books)
    if stats["count"] > 0:
        assert stats["min_rating"] <= stats["avg_rating"] <= stats["max_rating"]
        assert stats["rating_sum"] >= 0.0
