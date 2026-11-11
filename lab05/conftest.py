from collections.abc import Iterator

import pytest


@pytest.fixture
def sample_amounts() -> list[float]:
    return [100.0, -50.0, 200.0, -25.0, 300.0, -80.0, 150.0]


@pytest.fixture
def counting_generator() -> Iterator[int]:
    def _gen() -> Iterator[int]:
        i = 0
        while True:
            yield i
            i += 1

    return _gen()
