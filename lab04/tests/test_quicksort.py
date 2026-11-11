from algorithms import insertion_sort, quicksort_hybrid, quicksort_pure


def test_quicksort_pure() -> None:
    data = [9, 3, 7, 1, 8, 2, 5, 4, 6]
    assert quicksort_pure(data) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert quicksort_pure([]) == []
    assert quicksort_pure([42]) == [42]


def test_insertion_sort() -> None:
    data = [5, 1, 4, 2, 8]
    assert insertion_sort(data) == [1, 2, 4, 5, 8]


def test_quicksort_hybrid() -> None:
    data = [10 - i for i in range(30)]
    assert quicksort_hybrid(data, threshold=8) == sorted(data)
