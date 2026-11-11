from typing import Any

import pytest


@pytest.fixture
def nested_sample() -> list[Any]:
    return [1, [2, 3], (4, [5, (6, 7)]), [8, [9, [10]]]]
