from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class Num:
    val: float


@dataclass(frozen=True, slots=True)
class Add:
    left: Expr
    right: Expr


@dataclass(frozen=True, slots=True)
class Mul:
    left: Expr
    right: Expr


@dataclass(frozen=True, slots=True)
class Sub:
    left: Expr
    right: Expr


@dataclass(frozen=True, slots=True)
class Div:
    left: Expr
    right: Expr


Expr: TypeAlias = Num | Add | Mul | Sub | Div
