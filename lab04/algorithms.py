from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Generic, TypeVar

T = TypeVar("T")


def insertion_sort(seq: list[int]) -> list[int]:
    result = list(seq)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def quicksort_pure(seq: list[int]) -> list[int]:
    if len(seq) <= 1:
        return list(seq)
    pivot = seq[len(seq) // 2]
    left = [x for x in seq if x < pivot]
    mid = [x for x in seq if x == pivot]
    right = [x for x in seq if x > pivot]
    return quicksort_pure(left) + mid + quicksort_pure(right)


def quicksort_hybrid(seq: list[int], threshold: int = 16) -> list[int]:
    if len(seq) <= 1:
        return list(seq)
    if len(seq) <= threshold:
        return insertion_sort(seq)
    pivot = seq[len(seq) // 2]
    left = [x for x in seq if x < pivot]
    mid = [x for x in seq if x == pivot]
    right = [x for x in seq if x > pivot]
    return quicksort_hybrid(left, threshold) + mid + quicksort_hybrid(right, threshold)


@dataclass(frozen=True, slots=True)
class TreeNode(Generic[T]):
    val: T
    left: TreeNode[T] | None = None
    right: TreeNode[T] | None = None


def preorder(node: TreeNode[T] | None) -> list[T]:
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)


def inorder(node: TreeNode[T] | None) -> list[T]:
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)


def postorder(node: TreeNode[T] | None) -> list[T]:
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]


def fib_naive(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@cache
def fib_memoized(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)
