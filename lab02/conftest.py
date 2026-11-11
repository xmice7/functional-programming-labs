import pytest
from core import BookRecord


@pytest.fixture
def sample_books() -> list[BookRecord]:
    return [
        {
            "id": 1,
            "title": "The Hobbit",
            "genre": "Fantasy",
            "ratings": [4.8, 5.0, 4.6],
        },
        {
            "id": 2,
            "title": "Dune",
            "genre": "Sci-Fi",
            "ratings": [4.4, 4.6, 4.8],
        },
        {
            "id": 3,
            "title": "Clean Code",
            "genre": "Tech",
            "ratings": [3.5, 3.8, 3.2],
        },
        {
            "id": 4,
            "title": "The Fellowship of the Ring",
            "genre": "Fantasy",
            "ratings": [5.0, 4.9, 4.8],
        },
        {
            "id": 5,
            "title": "1984",
            "genre": "Classics",
            "ratings": [4.7, 4.8, 4.9],
        },
    ]
